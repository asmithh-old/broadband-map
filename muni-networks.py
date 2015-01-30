#TODO: load text of broadband penetration by metro area into usable format. [done]
#TODO: get list of cities with municipal networks.
#TODO: get demographic + physical characteristics of each city with census API.
#TODO: find out how broadband penetration differs between cities with and without municipal networks.

stateFips = {'01' : 'AL', '02' : 'AK', '60' : 'AS', '03' : 'AS', '04' : 'AZ', '05' : 'AR', '06' : 'CA', '08' : 'CO', '09' : 'CT', '10' : 'DE', '11' : 'DC', '12' : 'FL', '64' : 'FM', '13' : 'GA', '66' : 'GU', '15' : 'HI', '16' : 'ID', '17' : 'IL', '18' : 'IN', '19' : 'IA', '20' : 'KS', '21' : 'KY', '22' : 'LA', '23' : 'ME', '68' : 'MH', '24' : 'MD', '25' : 'MA', '26' : 'MI', '27' : 'MN', '28' : 'MS', '29' : 'MO', '30' : 'MT', '31' : 'NE', '32' : 'NV', '33' : 'NH', '34' : 'NJ', '35' : 'NM', '36' : 'NY', '37' : 'NC', '38' : 'ND', '69' : 'MP', '39' : 'OH', '40' : 'OK', '41' : 'OR', '70' : 'PW', '42' : 'PA', '72' : 'PR', '44' : 'RI', '45' : 'SC', '46' : 'SD', '47' : 'TN', '48' : 'TX', '74' : 'UM', '49' : 'UT', '50' : 'VT', '51' : 'VA', '78' : 'VI', '53' : 'WA', '54' : 'WV', '55' : 'WI', '56' : 'WY'}

import csv, re, nltk, urllib2, json, ast, numpy as np, matplotlib.pyplot as plt

metroAreasDict = {}
metroAreasBroadband = []
hasMuniNetwork = []
metroToFips = []

with open('metro-area-bb.csv', 'r') as f:
    #data for broadband penetration in metro areas. 
    lines = f.readlines()
    for line in lines:
        cities = line.split(',')[0].split('-')
        states = line.split(',')[1].split('-')
        states[0] = states[0][1:]
        #for every metro area possibly listed in the text file, we put the percentage of people who are using high-speed internet into the dictionary.  
        #this ensures that we have data for every possible name  
        for c in cities:
            for s in states:
                name = c + ' ' +  s
                name = re.sub('[0-9]', '', name)
                metroAreasBroadband.append(name)
                metroAreasDict[name] = {}
                metroAreasDict[name]['percent with high-speed internet'] = line.split(',')[2]
                
bbPen = {}     
bbPenbyFips = {}     
   
for m in metroAreasDict.keys():
    #for every metro area that has broadband penetration data, we want to get the population density and its geoId so we can match it up with the 
    #cities listed as having municipal networks and confirm its identity.  
    city = m
    stateName = city[-2:]
    city = city[0:-3]
    if ' ' in city:
        city = re.sub(' ', '%20', city)
    else:
        pass
    url = 'http://www.broadbandmap.gov/broadbandmap/demographic/dec2012/censusplace/names/' + city + '?format=json'
    try:
        resDict = json.loads(urllib2.urlopen(url).read())
        if 'Results' in resDict:
            if len(resDict['Results']) != 1:
                for r in resDict['Results']:
                    state = r['geographyId'][0:2]
                    geoId = r['geographyId']
                    if stateFips[state] == stateName:
                        bbPen[city] = {}
                        bbPen[city]['state'] = state
                        bbPen[city]['geoId'] = geoId
                        bbPen[city]['pop density'] = float(resDict['Results'][0]['population'])/float(resDict['Results'][0]['landArea'])
                        bbPen[city]['bb pen'] = metroAreasDict[m]
                        bbPenbyFips['geoId'] = city
    except:
        pass

hasMuniType = {}

with open('muni-networks.txt', 'r') as f:
    #list of metro areas with municipal broadband networks. keep track of municipal broadband types. (information isn't flowing through the intertubes with dark fiber yet)
    lines = f.readlines()
    for line in lines:
        lineCopy = line
        lumpy =  len(re.split('[A-Z]{2}', lineCopy)[0])
        myLine = line[0:lumpy+2]
        hasMuniType[myLine] = re.sub('\n', '', line).split(' ')[-1]
        
#get list of cities from muni-networks.
#match them to fips. 
#find places in metroAreasDict.keys() with matching demographic factors.
#compare their levels of broadband penetration.




fipsDict = {}
lookupByMSA = {}
allMetroFips = ''
with open('metro-areas-fips.txt') as f:
    #we try to match metro areas to FIPS codes to confirm lookup; mostly this does not work. the list may be hideously outdated.
    lines = f.readlines()
    for line in lines:
        if line != '\n':
            allMetroFips+= line + '!!!'
            placeName = re.sub(',|MSA|CMSA|PMSA|  +', '', re.findall("[A-Z][A-Za-z\- '()\.]+", line)[0])
            fipsDict[placeName] = {}
            fipsDict[placeName]['msa/cmsa fips'] = line[0:4]
            if line[0:4] in lookupByMSA:
                lookupByMSA[line[0:4]].append(placeName)
            else:
                lookupByMSA[line[0:4]] = []
                lookupByMSA[line[0:4]].append(placeName)
            fipsDict[placeName]['pmsa fips'] = line[8:12]
            fipsDict[placeName]['alt cmsa fips'] = line[16:19]
            fipsDict[placeName]['state/county fips'] = line[24:30]
            fipsDict[placeName]['central/outlying county or city/town flag'] = line[32:33]
            fipsDict[placeName]['city/town fips'] = line[40:45]
            
cityDemog = {}
for city in hasMuniType.keys():
    #we use the broadbandmap.gov api to look up data for population density. this is kind of feeling-around-in-the-dark-ish because
    #we are looking for matches for city names, some of which don't show up because they aren't census places, and some of which have 
    #multiple entries because they appear in multiple states or in multiple species in the same state. 
    cityName = city
    stateName = city[-2:]
    city = city[0:-3]
    if ' ' in city:
        city = re.sub(' ', '%20', city)
    else:
        pass
    url = 'http://www.broadbandmap.gov/broadbandmap/demographic/dec2012/censusplace/names/' + city + '?format=json'
    resDict = json.loads(urllib2.urlopen(url).read())
    if 'Results' in resDict:
        if len(resDict['Results']) != 1:
            for r in resDict['Results']:
                state = r['geographyId'][0:2]
                geoId = r['geographyId']
                if stateFips[state] == stateName:
                    #(is this the right metro area in the right state? i'm assuming naming collisions of cities within states are very unlikely)
                    if city + ' ' + stateName in cityDemog:
                        cityDemog[city + ' ' + stateName]['pop density'] = float(r['population'])/float(r['landArea'])
                        cityDemog[city + ' ' + stateName]['muni network'] = hasMuniType[cityName]
                        cityDemog[city + ' ' + stateName]['geoId'] = geoId
                    else:
                        cityDemog[city + ' ' + stateName] = {}
                        cityDemog[city + ' ' + stateName]['pop density'] = float(r['population'])/float(r['landArea'])
                        cityDemog[city + ' ' + stateName]['muni network'] = hasMuniType[cityName]
                        cityDemog[city + ' ' + stateName]['geoId'] = geoId
                        
                    #print 'True'
        else:
            if city + ' ' + stateName in cityDemog:
                cityDemog[city + ' ' + stateName]['pop density'] = float(resDict['Results'][0]['population'])/float(resDict['Results'][0]['landArea'])
                cityDemog[city + ' ' + stateName]['muni network'] = hasMuniType[cityName]
                cityDemog[city + ' ' + stateName]['geoId'] = geoId
                
            else:
                cityDemog[city + ' ' + stateName] = {}
                cityDemog[city + ' ' + stateName]['pop density'] = float(r['population'])/float(r['landArea'])
                cityDemog[city + ' ' + stateName]['muni network'] = hasMuniType[cityName]
                cityDemog[city + ' ' + stateName]['geoId'] = geoId
                
            
muniRhos = []   
muniPens = []
notMuniRhos = []
notMuniPens = []
deltas = []
hasMuniNames = []
notMuniNames = []

for c in cityDemog.keys():
    #for all places with muni networks, if the place has broadband penetration data available, find its population density and broadband penetration.
    #append those to lists so we can plot them later.
    #also find another city with comparable population density (as close as possible as long as it's not the same city) and get its broadband penetration percentage.
    #append those values to lists to be plotted as well.
    if c[0:-3] in bbPen:
        bestMatch = ''
        matchDist = float('inf')
        
        for e in bbPen.keys():
            if np.abs(bbPen[e]['pop density'] - cityDemog[c]['pop density']) < matchDist and e != c and e not in c:
                matchDist = np.abs(bbPen[e]['pop density'] - cityDemog[c]['pop density'])
                bestMatch = e
        print c, cityDemog[c]['pop density']
        muniRho = cityDemog[c]['pop density']
        try:
            print bbPen[re.sub('%20', ' ', c)[0:-3]]['bb pen']
            muniPen = bbPen[re.sub('%20', ' ', c)[0:-3]]['bb pen']['percent with high-speed internet']
        except:
            print "key error"
            
        print bestMatch, bbPen[bestMatch]['pop density']
        noMuniRho = bbPen[bestMatch]['pop density']
        try:
            print bbPen[bestMatch]['bb pen']
            noMuniPen = bbPen[bestMatch]['bb pen']['percent with high-speed internet']
        except:
            print "key error"
        print
        if muniPen != 'key error' and noMuniPen != 'key error' and cityDemog[c]['muni network']!= 'dark':
            #here we are only plotting pairs of tuples that have muni networks that aren't dark fiber (the fiber is installed but not operational yet)
            print cityDemog[c]['muni network']
            hasMuniNames.append(c)
            notMuniNames.append(bestMatch + ' ' + bbPen[bestMatch]['state'])
            muniRhos.append(float(muniRho))
            muniPens.append(float(muniPen))
            deltas.append(float(muniPen)-float(noMuniPen))
            notMuniRhos.append(float(noMuniRho))
            notMuniPens.append(float(noMuniPen))
            
print muniRhos
print
print muniPens
print
print notMuniRhos
print
print notMuniPens
print deltas
print hasMuniNames
print notMuniNames
#we plot log of population density (population density distributes according to log-normal distribution and also looks a lot more linear when it's a log plot...)
#versus percent of broadband penetration (defined as the percent of people subscribing to broadband internet.)
#plt.scatter(np.log2(muniRhos), muniPens, c = 'g')
#plt.scatter(np.log2(otMuniRhos), notMuniPens, c = 'r')
plt.scatter(np.log2(muniRhos), deltas, c='b')
plt.show()


