import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
#muniRhos = [1520.753608256806, 2177.600548985196, 921.1943479385027, 1733.3696352914574, 1305.6649518431798, 907.8561660952038, 1179.2210392545198, 1769.8509586674845, 986.5859404790097, 1736.6810099478673, 1586.748140674148, 2206.1946731819394, 1989.408585433394, 2207.9847873141134, 1322.5696433461094, 1727.1630897509185, 9979.11219800748, 1226.1158292648304, 1533.5327555117453, 1681.3438904978584, 336.9140357967581, 996.929464629918, 3101.8603528384347, 4041.949429273698, 1067.4220784546642, 834.8681563682649, 2727.440811432808, 1856.9285723906758, 685.7009387282695, 1160.476945438877, 2065.879880353248, 4132.665580300787, 3566.045909725897, 1371.0782964011212, 862.1368538026926, 1031.925596434427, 795.928462608548, 3551.4128170838962, 5271.694063429893, 1583.4256301757234, 2161.6879542423703, 3464.1668944002213, 3148.139195383356, 4315.073341121866, 2664.137926457671, 1865.0826086467152, 7358.635071932757, 2526.58879796881, 2657.9564784628988, 871.7708257874895, 1404.983115627842, 1603.0876494321344, 2207.4194597986548, 1192.952505100167, 1747.8753504986923, 5426.2925239267715, 1695.048183838169, 993.9842054511548, 1785.5697910608515, 5221.838670773027, 612.1181270458519, 2973.966920694535, 5189.694195547119]

#muniPens = [84.3, 85.2, 80.8, 93.8, 85.2, 82.2, 89.9, 88.9, 82.2, 82.2, 78.9, 92.1, 86.9, 87.5, 81.8, 88.3, 88.3, 84.3, 87.7, 87.7, 87.6, 88.5, 88.5, 91.4, 75.5, 84.3, 86.7, 84.6, 89.5, 87.6, 89.1, 89.4, 89.1, 83.2, 87.6, 87.6, 83.2, 90.8, 94.3, 88.8, 82.4, 84.3, 87.0, 92.1, 93.3, 92.5, 92.5, 91.1, 91.1, 89.3, 83.1, 81.8, 81.8, 80.1, 89.0, 91.8, 94.3, 89.5, 89.5, 78.9, 92.5, 87.3, 92.9]

noMuniRhos = [1522.4875406147128, 2157.2212767906703, 920.145236488475, 1729.3404554326319, 1303.330693326029, 902.4767781376797, 1166.8956072998963, 1763.1593355669847, 987.1450586152565, 1741.2430898481566, 1597.9783215470252, 2202.561052461886, 1997.1030062400894, 2202.561052461886, 1315.1376249277546, 1728.3931398969203, 9461.264858017817, 1271.405979025319, 1531.9141161371817, 1683.128514543846, 337.90833279758164, 1000.2030436794001, 3122.4630737784937, 3929.2659321002357, 1070.4740841486557, 831.157921486354, 2724.563435585714, 1861.1319943496992, 689.3642192399585, 1163.8112975533177, 2079.312182736265, 4041.949429273698, 3607.4127302144784, 1370.4727622688663, 861.9160334388, 1032.3240871539763, 792.4999873454633, 3607.4127302144784, 5222.661956498442, 1569.334130251285, 2157.2212767906703, 3458.458371035701, 3122.4630737784937, 4312.973052699587, 2657.9564784628988, 1866.7561077942432, 7356.9625215878905, 2529.4387086215934, 2629.4099337824473, 875.4505346695378, 1433.9018017445587, 1597.9783215470252, 2202.561052461886, 1166.8956072998963, 1753.3030014240037, 5466.633412022233, 1691.1444453016538, 1000.2030436794001, 1780.8210432481317, 5222.661956498442, 616.8522117338896, 2968.566378445419, 5222.661956498442]

noMuniPens = [89.4, 89.3, 83.6, 90.1, 86.7, 86.9, 81.8, 89.5, 88.1, 86.7, 83.6, 85.2, 89.1, 85.2, 93.6, 95.1, 92.9, 81.3, 87.0, 88.6, 85.8, 87.0, 92.1, 75.6, 83.6, 69.3, 83.9, 88.1, 75.7, 88.8, 87.6, 91.4, 87.3, 86.4, 89.3, 90.1, 88.6, 87.3, 87.5, 91.8, 89.3, 92.0, 92.1, 90.2, 86.6, 81.8, 87.9, 82.2, 95.7, 85.5, 89.3, 83.6, 85.2, 81.8, 92.5, 93.4, 79.6, 87.0, 89.5, 87.5, 93.4, 88.9, 87.5]

muniRhos = [1520.753608256806, 2177.600548985196, 1733.3696352914574, 1305.6649518431798, 907.8561660952038, 1769.8509586674845, 986.5859404790097, 1586.748140674148, 2206.1946731819394, 2207.9847873141134, 1727.1630897509185, 1226.1158292648304, 1533.5327555117453, 1681.3438904978584, 996.929464629918, 3101.8603528384347, 4041.949429273698, 1067.4220784546642, 834.8681563682649, 2727.440811432808, 1856.9285723906758, 685.7009387282695, 1160.476945438877, 2065.879880353248, 4132.665580300787, 3566.045909725897, 1371.0782964011212, 862.1368538026926, 1031.925596434427, 795.928462608548, 5271.694063429893, 1583.4256301757234, 2161.6879542423703, 3464.1668944002213, 3148.139195383356, 2664.137926457671, 7358.635071932757, 871.7708257874895, 1603.0876494321344, 2207.4194597986548, 1192.952505100167, 1747.8753504986923, 5426.2925239267715, 993.9842054511548, 1785.5697910608515, 5221.838670773027, 2973.966920694535]

muniPens = [84.3, 85.2, 93.8, 85.2, 82.2, 88.9, 82.2, 78.9, 92.1, 87.5, 88.3, 84.3, 87.7, 87.7, 88.5, 88.5, 91.4, 75.5, 84.3, 86.7, 84.6, 89.5, 87.6, 89.1, 89.4, 89.1, 83.2, 87.6, 87.6, 83.2, 94.3, 88.8, 82.4, 84.3, 87.0, 93.3, 92.5, 89.3, 81.8, 81.8, 80.1, 89.0, 91.8, 89.5, 89.5, 78.9, 87.3]

#noMuniRhos = [1522.4875406147128, 2157.2212767906703, 1729.3404554326319, 1303.330693326029, 902.4767781376797, 1763.1593355669847, 987.1450586152565, 1597.9783215470252, 2202.561052461886, 2202.561052461886, 1728.3931398969203, 1271.405979025319, 1531.9141161371817, 1683.128514543846, 1000.2030436794001, 3122.4630737784937, 3929.2659321002357, 1070.4740841486557, 831.157921486354, 2724.563435585714, 1861.1319943496992, 689.3642192399585, 1163.8112975533177, 2079.312182736265, 4041.949429273698, 3607.4127302144784, 1370.4727622688663, 861.9160334388, 1032.3240871539763, 792.4999873454633, 5222.661956498442, 1569.334130251285, 2157.2212767906703, 3458.458371035701, 3122.4630737784937, 2657.9564784628988, 7356.9625215878905, 875.4505346695378, 1597.9783215470252, 2202.561052461886, 1166.8956072998963, 1753.3030014240037, 5466.633412022233, 1000.2030436794001, 1780.8210432481317, 5222.661956498442, 2968.566378445419]

#noMuniPens = [89.4, 89.3, 90.1, 86.7, 86.9, 89.5, 88.1, 83.6, 85.2, 85.2, 95.1, 81.3, 87.0, 88.6, 87.0, 92.1, 75.6, 83.6, 69.3, 83.9, 88.1, 75.7, 88.8, 87.6, 91.4, 87.3, 86.4, 89.3, 90.1, 88.6, 87.5, 91.8, 89.3, 92.0, 92.1, 86.6, 87.9, 85.5, 83.6, 85.2, 81.8, 92.5, 93.4, 87.0, 89.5, 87.5, 88.9]

#(slope, intercept) = stats.linregress(np.log2(muniRhos), muniPens)[0:2]

print stats.mstats.theilslopes(muniPens, np.log2(muniRhos))

#slope = 0.02679735
#intercept = 6.16532264
#slope = 0.02821452
#intercept = 6.14936165
slope = 1.75060757
intercept = 68.76910629

plt.plot(np.log2(muniRhos), slope * np.log2(muniRhos) + intercept * np.ones(len(muniRhos)), c = "g")

#(slope, intercept) = stats.linregress(np.log2(noMuniRhos), noMuniPens)[0:2]
print stats.mstats.theilslopes(noMuniPens, np.log2(noMuniRhos))

#slope = 0.01911137
#intercept = 6.24637843
#slope = 0.01911137
#intercept = 6.24637843
slope = 1.19120122
intercept = 74.73153844

plt.plot(np.log2(noMuniRhos), slope * np.log2(noMuniRhos) + intercept * np.ones(len(noMuniRhos)), c = "r")

plt.plot(np.log2(muniRhos), muniPens, c = "g", marker = "^", ls = "none")
plt.plot(np.log2(noMuniRhos),noMuniPens, c = "r", marker = "o", ls = "none")
plt.xlabel('binary logarithm of population density')
plt.ylabel('percent broadband penetration')
plt.show()