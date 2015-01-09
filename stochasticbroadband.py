import urllib2, json, ast
import numpy as np

counties = []
providerNums = {}
hasBroadband = {}
with open('counties.txt') as f:
    content = f.readlines()
#gets list of counties from text list of counties.

for line in content[1:]:
    code = line[3:5] + line[6:9]
    #print code
    counties.append(code)
    providerNums[code] = {}
    times = ['jun2011', 'dec2011', 'jun2012', 'dec2012']
    hasBroadband[code] = {}
    for time in times:
        hasBroadband[code][time] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}
    #initializes lists of numbers of broadband providers at different times in each county.
    
with open('countydata.txt') as g:
    
    foo = g.readlines()
    #print foo
    conditional = ast.literal_eval(foo[0])
    print type(conditional)
    countyDemog = ast.literal_eval(foo[1])
    print type(countyDemog)
    #g.readlines()[1]
    #gets data created in broadbandmap.py for use later on
    
batched = []  
lumpy = len(counties)
print lumpy
i = 0
while i < lumpy-10:
    florp = []
    for j in range(0, 10):
        florp.append(counties[i])
        i += 1
    batched.append(florp)
    #once again, i'm assuming it's optimal to query the api in batches of maximum size
    

rhoMean = 6.0
rhoSigma = 3.33
rhoDict = {'minus3': [], 'minus2': [], 'minus1': [], 'plus1' : [], 'plus2' : [], 'plus3' : []}
giniMean = 0.43
giniSigma = 0.063
giniDict = {'minus3': [], 'minus2': [], 'minus1': [], 'plus1' : [], 'plus2' : [], 'plus3' : []}
#divide entropies into sections of 0.2 from 0 to 1, then greater than 1.
entropyStep = 0.2
entropyMax = 1.0
entropyDict = {0 : [], 1 : [], 2 : [], 3 : [], 4 : [], 5 : [] }
#foo = raw_input('')
#i need a way to stick communities into 'bins' based on their characteristics. 
#since gini index is Gaussian, we can index the gini index based on how many standard deviations it is from the mean of .43
#similarly the log of population density is gaussian so we can bin it with the same function.
#entropy is kind of evenly distributed so we just divide it into 5 approximately equal sections. this may not be as valid as the way i binned the gaussians so if you're going to change a binning that'd probably be it.

def gaussian_bin_var(var, varMean, varSigma, varDict):
    #bins value based on the distance (in standard deviations) it is from the mean

    if var < varMean - 2.0 * varSigma:
        varDict['minus3'].append(rho)
        return -3
    elif var < varMean - 1.0 * varSigma:
        varDict['minus2'].append(var)
        return -2
    elif var < varMean:
        varDict['minus1'].append(var)
        return -1
    elif var < varMean + 1.0 * varSigma:
        varDict['plus1'].append(var)
        return 1
    elif var < varMean + 2.0 * varSigma:
        varDict['plus2'].append(var)
        return 2
    elif var >= varMean + 2.0 * varSigma:
        varDict['plus3'].append(var)
        return 3
        
def sketchy_bin_var(var, step, maxVal, varDict):
    #bins variable based on simple linear divisions at equal intervals.
    marker = 0.0
    iteration = 0
    #print var
    while marker < maxVal and marker < var:
        marker += step
        iteration += 1
        #print iteration
    #print
    try:
        entropyDict[iteration - 1].append(var)
    except KeyError:
        if var == -0.0:
            iteration = 1
            entropyDict[iteration - 1].append(var)
    return iteration - 1
    

times = ['jun2011', 'dec2011', 'jun2012', 'dec2012']
for batch in batched:
    #for each county, gets the percent of households with n broadband providers for n in [0:8] at all times in times.
    
    # dec2012, jun2012, dec2011, jun2011
    #numberOfWirelineProvidersEquals0":0.01040,"numberOfWirelineProvidersEquals1":0.04540,"numberOfWirelineProvidersEquals2":0.50750,"numberOfWirelineProvidersEquals3":0.36440,"numberOfWirelineProvidersEquals4":0.06590,"numberOfWirelineProvidersEquals5":0.00570,"numberOfWirelineProvidersEquals6":0.00070,"numberOfWirelineProvidersEquals7":0.00000,"numberOfWirelineProvidersGreaterThan8":0.00000 
    #print batch
    for timeStamp in times:
        url = 'http://www.broadbandmap.gov/broadbandmap/analyze/'
        url += timeStamp
        url += '/summary/population/county/ids/'
        for county in batch:
            url += str(county) + ','
        url += '?format=json'
        #print url
        fileobj = urllib2.urlopen(url)
        #print url
        timeResponse = json.loads(fileobj.read())
        #timeResponse['Results'] is a list of dictionaries containing all the information you could ever want about 
        #broadband access in a given community
        
        #print len(timeResponse['Results'])

        for countyData in timeResponse['Results']:
            #print type(countyData)
            countyData = countyData
            #providerNums[countyData['geographyId']][timeStamp] contains the average (estimated) number of providers at time timeStamp for FIPs code countyData['geographyId']
            providerNums[countyData['geographyId']][timeStamp] = round(0.0 * countyData['numberOfWirelineProvidersEquals0'] + 1.0 * countyData['numberOfWirelineProvidersEquals1'] + 2.0 * countyData['numberOfWirelineProvidersEquals2'] + 3.0 * countyData['numberOfWirelineProvidersEquals3'] + 4.0 * countyData['numberOfWirelineProvidersEquals4'] + 5.0 * countyData['numberOfWirelineProvidersEquals5'] + 6.0 * countyData['numberOfWirelineProvidersEquals6'] + 7.0 * countyData['numberOfWirelineProvidersEquals7'] + 9.0 * countyData['numberOfWirelineProvidersGreaterThan8'])
            for t in range(0, 8):
                keyStr = 'numberOfWirelineProvidersEquals' + str(t)
                hasBroadband[countyData['geographyId']][timeStamp][t] = countyData[keyStr]
            hasBroadband[countyData['geographyId']][timeStamp][8] = countyData['numberOfWirelineProvidersGreaterThan8']
            #hasBroadband contains the following distribution: for n in range[0:8], what percent of households can choose between n providers?
            
empiricalTransitions = {}
totals = {}
for i in range(0, 11):
    totals[i] = 0
    for j in range(0, 11):
        empiricalTransitions[(i, j)] = 0
        
conditionalTransitions =  {}   
for r in [-3, -2, -1, 1, 2, 3]:
    for g in [-3, -2, -1, 1, 2, 3]:
        for h in [0, 1, 2, 3, 4, 5, 6]:
            conditionalTransitions[(r, g, h)] = {}
            for i in range(0, 11):
                for j in range(0, 11):
                    conditionalTransitions[(r, g, h)][(i, j)] = 0
                        
#initialize data structs empiricalTransitions, which stores number of transitions from i providers to j providers and conditionalTransitions, the number of transitions from i providers to j providers in communities with (r, g, h) characteristics (population density, gini index, racial entropy)

#next block of code finds each county's binning and distribution of provider numbers for each timestamp provided and populates the probability tables accordingly.

transitionList = [('jun2011', 'dec2011'), ('dec2011', 'jun2012'), ('jun2012', 'dec2012')]    
for county in counties:
    try:
        
        (rho, gini, entropy) = countyDemog[county]
        r = gaussian_bin_var(np.log2(rho), rhoMean, rhoSigma, rhoDict)
        g = gaussian_bin_var(gini, giniMean, giniSigma, giniDict)
        h = sketchy_bin_var(entropy, entropyStep, entropyMax, entropyDict)
    except KeyError:
        print county
        #print providerNums[county]
        
        
    
    try:
        for (start, end) in transitionList:
            x = providerNums[county][start]
            y = providerNums[county][end]
            totals[x] += 1
            empiricalTransitions[(x,y)]  += 1
            conditionalTransitions[(r, g, h)][(x,y)] += 1
    except KeyError:
        print county
        #print providerNums[county]
    print conditionalTransitions[(r,g,h)]
    print
    

#writes data tables to a text file for easy retrieval    
with open('stochasticbroadband.txt', 'w') as z:
    z.write(str(empiricalTransitions))
    z.write(str('\n'))
    z.write(str(totals))
    z.write(str('\n'))
    z.write(str(conditionalTransitions))
    z.write(str('\n'))
    z.write(str(hasBroadband))
    z.write(str('\n'))
    z.write(str(countyDemog))
    z.close()

