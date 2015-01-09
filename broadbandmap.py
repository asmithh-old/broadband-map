import urllib2, json, random, itertools, csv
import numpy as np
import matplotlib.pyplot as plt



possibleCounties = []
with open('counties.txt') as f:
    #counties.txt is a list of counties and their county codes.
    content = f.readlines()
for line in content[1:]:
    code = line[3:5] + line[6:9]
    #print code
    possibleCounties.append(code)
 
counties = []  
lumpy = len(possibleCounties)
print lumpy
i = 0

while i < lumpy-10:
    #to make most efficient use of the broadbandmap.gov api, we query the api in batches of 10 counties (the maximum number of queries allowed at once), so we need a list of batches to iterate through. this acts on the assumption that there is a nontrivial constant cost to query the api, and a smaller additional cost per county queried; therefore it is most efficient to query by the largest possible batch size.
    florp = []
    for j in range(0, 10):
        florp.append(possibleCounties[i])
        #print i
        i += 1
    counties.append(florp)
 

giniTotal = 0
ginis = []
entropyTotal = 0
entropies = []
rhoTotal = 0
rhos = []
internetTotal = 0

def careful_log(number):
    #taking the log of things can be difficult. the numpy log2 function is good at taking the log of small fractions accurately, but it freaks out with 0 as an input. by convention we will assume log2(0) = 0. 
    if number == 0:
        return -0.0
    else:
        return np.log2(number)
        
allCounties = {}
internetPoints = {}

for batch in counties:
    
    url = 'http://www.broadbandmap.gov/broadbandmap/demographic/dec2012/county/ids/'
    for county in batch:
        url += str(county) + ','
    url += '?format=json'
    fileobj = urllib2.urlopen(url)
    #print url
    allResponse = json.loads(fileobj.read())
    #queries broadband.gov for demographics based on census data and loads it into a list of responses by county in the batch
    
    nexturl = 'http://www.broadbandmap.gov/broadbandmap/analyze/dec2012/summary/population/county/ids/'
    for county in batch:
        nexturl += str(county) + ','
    nexturl += '?format=json'
    nextfileobj = urllib2.urlopen(nexturl)
    broadband = json.loads(nextfileobj.read())
    #queries broadband.gov for broadband data based on census data and loads it into a list of responses by county in the batch
    
    for (i, bro) in itertools.izip(allResponse['Results'], broadband['Results']):
        #calculating gini index of the community and broadband access percentages.
        geoId = i['geographyId']
        #geoId is the FIPS code for the county in question
        
        contriblt25 = i['incomeLessThan25'] * 12500.0 
        contrib25to50 = i['incomeBetween25to50']*37500.0
        contrib50to100 = i['incomeBetween50to100']*75000.0
        contrib100to200 = i['incomeBetween100to200']*150000.0
        contrib200up = 600000.0 * i['incomeGreater200']
        #these are incredibly fudge-y but they also return the correct average national gini index so i guess it worked.
        #i visualized the area under the economic contribution curve as a series of triangles and trapezoids. 
        #for each income bracket, the height of the trapezoid is the percent of the population in that income bracket. the slope 
        #is the average income of that bracket (guesstimated). we then have the area under the curve, and we know the area under
        #the line of equality is 1. from there it is easy to calculate the gini index.
        #this is a lot easier than integration....
        
        
        totalIncome = contriblt25 + contrib25to50 + contrib50to100 + contrib100to200 + contrib200up
        if totalIncome == 0:
            print "no monies"
            break
        
        sharelt25 = contriblt25/totalIncome
        share25to50 = contrib25to50/totalIncome
        share50to100 = contrib50to100/totalIncome
        share100to200 = contrib100to200/totalIncome
        share200up = contrib200up/totalIncome
        
        giniB = sharelt25 * 0.5 * i['incomeLessThan25']
        giniB += sharelt25 * i['incomeBetween25to50'] + 0.5 * share25to50 * i['incomeBetween25to50']
        giniB += (sharelt25 + share25to50) * i['incomeBetween50to100'] + 0.5 * share50to100 * i['incomeBetween50to100']
        giniB += (sharelt25 + share25to50 + share50to100) * i['incomeBetween100to200'] + 0.5 * share100to200 * i['incomeBetween100to200']
        giniB += (sharelt25 + share25to50 + share50to100 + share100to200) * i['incomeGreater200'] + 0.5 * share200up * i['incomeGreater200']
        
        gini = 1.0 - 2 * giniB
        giniTotal += gini
        ginis.append(gini)
        #print gini
        
        #calculate the shannon entropy of the distribution of races in bits. 
        entropy = i['raceBlack'] * careful_log(i['raceBlack']) + i['raceWhite'] * careful_log(i['raceWhite']) + i['raceHispanic'] * careful_log(i['raceHispanic']) + i['raceAsian'] * careful_log(i['raceAsian']) * i['raceNativeAmerican'] * careful_log(i['raceNativeAmerican'])
        entropy *= -1
        entropyTotal += entropy
        entropies.append(entropy)
        #print entropy
        
        #rho is the population density per unit land area (miles or km? i forgot. probably km if they are sensible but who knows)
        rho = float(i['population'])/i['landArea']
        rhoTotal += rho
        rhos.append(rho)
        #print rho
        
        #bins the percent of people with broadband internet by flooring to the nearest 10%
        percentBroadband = bro['downloadSpeedGreaterThan3Mbps']
        internet = int(percentBroadband * 1000) / 100
        internetTotal += internet
        
        internetPoints[(rho, gini, entropy)] = internet
        #indexes the point (rho, gini, entropy) to the percent of people with broadband
        allCounties[geoId] = (rho, gini, entropy)
        #indexes geographic ID (FIPS code) to demographic figures
print len(allCounties.keys())
print len(internetPoints.keys())       
rprime = 0
gprime = 0
hprime = 0
divisions = 5
rdeltas = divisions * [(0,0)]
gdeltas = divisions * [(0,0)]
hdeltas = divisions * [(0,0)]

    
#plt.hist(np.log2(rhos), bins = 30)
#urrk
#plt.show()
#plt.hist(ginis, bins = 30)
#gaussian
##plt.show()
#plt.hist(np.log2(entropies), bins = 30)
#see screenshot
#plt.show()

#i need a way to stick communities into 'bins' based on their characteristics. 
#since gini index is Gaussian, we can index the gini index based on how many standard deviations it is from the mean of .43
#similarly the log of population density is gaussian so we can bin it with the same function.
#entropy is kind of evenly distributed so we just divide it into 5 approximately equal sections. this may not be as valid as the way i binned the gaussians so if you're going to change a binning that'd probably be it.

#also i should probably mention that these means and divisions are estimated from plotted histograms; if you uncomment the chunk of code above you can see the histograms.
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
    
quadrants = {}
joint = {}
conditional = {}
        
for r in [-3, -2, -1, 1, 2, 3]:
    for g in [-3, -2, -1, 1, 2, 3]:
        for h in [0, 1, 2, 3, 4, 5, 6]:
            #initialize dictionaries that will hold distributions.
            #quadrants will be the probability that a county falls into that binning (P(r, g, h))
            #joint will be the probability of a county with binning (r, g, h) and broadband access (i)
            #conditional (based on chain rule of probability) is P(i, r, g, h)/P(r, g, h)
            quadrants[(r, g, h)] = 0
            joint[(r, g, h)] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
            conditional[(r, g, h)] = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}

for key in allCounties.keys():
    (rho, gini, entropy) = allCounties[key]
    i = internetPoints[(rho,gini,entropy)]
    r = gaussian_bin_var(np.log2(rho), rhoMean, rhoSigma, rhoDict)
    g = gaussian_bin_var(gini, giniMean, giniSigma, giniDict)
    h = sketchy_bin_var(entropy, entropyStep, entropyMax, entropyDict)
    #bins variables and generates probabilites based on binnings.
    quadrants[(r,g,h)] = quadrants[(r, g, h)] + 1
    joint[(r,g,h)][i] = joint[(r, g, h)][i] + 1


    
for key in quadrants.keys():
    prior = quadrants[key]
    
    #creates conditional distributions; attempts to normalize probabilites but i think they're broken a little bit
    #TODO: fix normalization.
        
    quadrants[key] = float(prior)/float(lumpy) #P(r, g, h)
    
    for internet in joint[key].keys():
        if prior == 0:
            joint[key][internet] = 0
            conditional[key][internet] = 0
        else:
            joint[key][internet] = float(joint[key][internet])/float(prior) #P(i, r, g, h)
            conditional[key][internet] = float(joint[key][internet])/float(quadrants[key])

with open('countydata.txt', 'w') as f:
    f.write(str(conditional)) 
    f.write('\n')   
    f.write(str(allCounties))
    #writes data to text file so it will be usable later in other computations without recomputing everything above.

#rgh
keepGoing = True
          

                
while keepGoing:
    try:
        county = raw_input('county code? type "no" to input statistics')
        if county != "no":
            (rho, gini, entropy) = allCounties[county]
        else:
            rho = input('population density?')
            gini = input('gini index?')
            entropy = input('race entropy?')
    except KeyError:
        print "not in counties :("
    r = gaussian_bin_var(np.log2(rho), rhoMean, rhoSigma, rhoDict)
    g = gaussian_bin_var(gini, giniMean, giniSigma, giniDict)
    h = sketchy_bin_var(entropy, entropyStep, entropyMax, entropyDict)
    print
    try:
        print conditional[(r, g, h)]
    except KeyError:
        print r == 3
    stop = raw_input('if you want to stop, type "stop"')
    if stop == "stop":
        keepGoing = False
    
#this is the user interaction part of things.

         
                              
            
            
            