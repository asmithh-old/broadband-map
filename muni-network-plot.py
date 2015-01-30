import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import re
#you don't actually need scipy

stateFips = {'01' : 'AL', '02' : 'AK', '60' : 'AS', '03' : 'AS', '04' : 'AZ', '05' : 'AR', '06' : 'CA', '08' : 'CO', '09' : 'CT', '10' : 'DE', '11' : 'DC', '12' : 'FL', '64' : 'FM', '13' : 'GA', '66' : 'GU', '15' : 'HI', '16' : 'ID', '17' : 'IL', '18' : 'IN', '19' : 'IA', '20' : 'KS', '21' : 'KY', '22' : 'LA', '23' : 'ME', '68' : 'MH', '24' : 'MD', '25' : 'MA', '26' : 'MI', '27' : 'MN', '28' : 'MS', '29' : 'MO', '30' : 'MT', '31' : 'NE', '32' : 'NV', '33' : 'NH', '34' : 'NJ', '35' : 'NM', '36' : 'NY', '37' : 'NC', '38' : 'ND', '69' : 'MP', '39' : 'OH', '40' : 'OK', '41' : 'OR', '70' : 'PW', '42' : 'PA', '72' : 'PR', '44' : 'RI', '45' : 'SC', '46' : 'SD', '47' : 'TN', '48' : 'TX', '74' : 'UM', '49' : 'UT', '50' : 'VT', '51' : 'VA', '78' : 'VI', '53' : 'WA', '54' : 'WV', '55' : 'WI', '56' : 'WY'}

hasMuniNames = ['Anderson IN', 'Burlington WA', 'Bellevue IA', 'Chattanooga TN', 'Bristol TN', 'Easton MD', 'Morganton NC', 'Cleveland VA', 'Springfield MO', 'Wausau WI', 'Salisbury NC', 'Mansfield WA', 'Conway AR', 'Johnson%20City TN', 'Vineland NJ', 'Chapel%20Hill NC', 'Urbana IL', 'Danville VA', 'Greenville TX', 'Lafayette LA', 'Dalton GA', 'Fayetteville TN', 'Lebanon IN', 'Auburn IN', 'Cincinnati OH', 'Akron OH', 'Jackson TN', 'Lebanon VA', 'Monroe GA', 'Jackson MN', 'Manchester CT', 'Clarksville TN', 'Gainesville FL', 'Ashland OR', 'Canton OH', 'Bridgeport WA', 'Santa%20Clara CA', 'Franklin KY', 'Marion VA', 'Eau%20Claire WI', 'Morristown TN', 'Bryan OH', 'Worcester MA', 'Jacksonville FL', 'Bowling%20Green KY', 'Cleveland OH', 'Elyria OH']

notMuniNames = [u'Sherman 48', u'Richmond 51', u'Troy 36', u'Jefferson%20City 29', u'Hanover 42', u'Rogers 05', u'Kingman 04', u'Youngstown 42', u'Pueblo 08', u'Pueblo 08', u'Logan 49', u'Yuma 04', u'Canton 39', u'Sebastian 12', u'San%20Antonio 48', u'Carlsbad 06', u'Mission 48', u'Elkhart 18', u'Laredo 48', u'Memphis 47', u'La%20Porte 18', u'Sebring 12', u'Huntsville 01', u'Lebanon 42', u'Urbana 17', u'Mesa 04', u'Montgomery 01', u'Lima 39', u'Newark 34', u'Santa%20Fe 35', u'Stockton 06', u'Norwich 09', u'Richmond 51', u'Round%20Rock 48', u'Carlsbad 06', u'South%20Bend 18', u'New%20Haven 09', u'Hazleton 42', u'Youngstown 42', u'Pueblo 08', u'Waynesboro 51', u'Rochester 27', u'Oakland 06', u'San%20Antonio 48', u'Bismarck 38', u'Stockton 06', u'Moline 17']
muniRhos = [1520.753608256806, 2177.600548985196, 1733.3696352914574, 1305.6649518431798, 907.8561660952038, 1769.8509586674845, 986.5859404790097, 1586.748140674148, 2206.1946731819394, 2207.9847873141134, 1727.1630897509185, 1226.1158292648304, 1533.5327555117453, 1681.3438904978584, 996.929464629918, 3101.8603528384347, 4041.949429273698, 1067.4220784546642, 834.8681563682649, 2727.440811432808, 1856.9285723906758, 685.7009387282695, 1160.476945438877, 2065.879880353248, 4132.665580300787, 3566.045909725897, 1371.0782964011212, 862.1368538026926, 1031.925596434427, 795.928462608548, 5271.694063429893, 1583.4256301757234, 2161.6879542423703, 3464.1668944002213, 3148.139195383356, 2664.137926457671, 7358.635071932757, 871.7708257874895, 1603.0876494321344, 2207.4194597986548, 1192.952505100167, 1747.8753504986923, 5426.2925239267715, 993.9842054511548, 1785.5697910608515, 5221.838670773027, 2973.966920694535]

muniPens = [84.3, 85.2, 93.8, 85.2, 82.2, 88.9, 82.2, 78.9, 92.1, 87.5, 88.3, 84.3, 87.7, 87.7, 88.5, 88.5, 91.4, 75.5, 84.3, 86.7, 84.6, 89.5, 87.6, 89.1, 89.4, 89.1, 83.2, 87.6, 87.6, 83.2, 94.3, 88.8, 82.4, 84.3, 87.0, 93.3, 92.5, 89.3, 81.8, 81.8, 80.1, 89.0, 91.8, 89.5, 89.5, 78.9, 87.3]

noMuniRhos = [1522.4875406147128, 2157.2212767906703, 1729.3404554326319, 1303.330693326029, 902.4767781376797, 1763.1593355669847, 987.1450586152565, 1597.9783215470252, 2202.561052461886, 2202.561052461886, 1728.3931398969203, 1271.405979025319, 1531.9141161371817, 1683.128514543846, 1000.2030436794001, 3122.4630737784937, 3929.2659321002357, 1070.4740841486557, 831.157921486354, 2724.563435585714, 1861.1319943496992, 689.3642192399585, 1163.8112975533177, 2079.312182736265, 4041.949429273698, 3607.4127302144784, 1370.4727622688663, 861.9160334388, 1032.3240871539763, 792.4999873454633, 5222.661956498442, 1569.334130251285, 2157.2212767906703, 3458.458371035701, 3122.4630737784937, 2657.9564784628988, 7356.9625215878905, 875.4505346695378, 1597.9783215470252, 2202.561052461886, 1166.8956072998963, 1753.3030014240037, 5466.633412022233, 1000.2030436794001, 1780.8210432481317, 5222.661956498442, 2968.566378445419]

noMuniPens = [89.4, 89.3, 90.1, 86.7, 86.9, 89.5, 88.1, 83.6, 85.2, 85.2, 95.1, 81.3, 87.0, 88.6, 87.0, 92.1, 75.6, 83.6, 69.3, 83.9, 88.1, 75.7, 88.8, 87.6, 91.4, 87.3, 86.4, 89.3, 90.1, 88.6, 87.5, 91.8, 89.3, 92.0, 92.1, 86.6, 87.9, 85.5, 83.6, 85.2, 81.8, 92.5, 93.4, 87.0, 89.5, 87.5, 88.9]

slope = 1.75060757
intercept = 68.76910629

slope = 1.19120122
intercept = 74.73153844

ratios = []
count = 0
for i in notMuniNames:
    i = i[0:-3] + ' ' + stateFips[i[-2:]]
    i = re.sub('%20', ' ', i)
    notMuniNames[count] = i
    count += 1
    
count = 0
for i in hasMuniNames:
    i = re.sub('%20', ' ', i)
    hasMuniNames[count] = i
    count += 1
for i in range(len(muniPens)):
    ratios.append(muniPens[i]/noMuniPens[i])
#plt.plot(np.log2(muniRhos), muniPens, c = "g", marker = "^", ls = "none")
#plt.plot(np.log2(noMuniRhos),noMuniPens, c = "r", marker = "o", ls = "none")

plt.plot(np.log2(muniRhos), ratios, c = "b", marker = "^", ls = "none")

#for i in range(len(muniPens)):
    #plt.annotate(xy = (np.log2(muniRhos[i]), muniPens[i]),s = hasMuniNames[i] )
#for j in range(len(noMuniPens)-1):
    #plt.annotate(xy = (np.log2(noMuniRhos[j]), noMuniPens[j]), s = notMuniNames[j])
m = 0.00183666
b = 0.96207448
plt.plot(np.log2(muniRhos), m * np.log2(muniRhos) + np.ones(len(muniRhos))* b, c = "g", marker = "o")
print stats.mstats.theilslopes(ratios, np.log2(muniRhos))
for j in range(len(muniPens)):

    plt.annotate(xy = (np.log2(muniRhos[j]), ratios[j]), s = hasMuniNames[j] + ', '+ notMuniNames[j] )

plt.xlabel('binary logarithm of population density')
#plt.ylabel('percent broadband penetration')
plt.ylabel('muni:not muni pen ratio')
plt.show()