import numpy as np
import ast
from sklearn.preprocessing import normalize

with open('stochasticbroadband.txt') as f:
    lines = f.readlines()
    empiricalTransitions = ast.literal_eval(lines[0])
    totals = ast.literal_eval(lines[1])
    conditionalTransitions = ast.literal_eval(lines[2])
    hasBroadband = ast.literal_eval(lines[3])
    countyDemog = ast.literal_eval(lines[4])
    
print type(empiricalTransitions)
print type(totals)
print type(conditionalTransitions)

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
        varDict[iteration - 1].append(var)
    except KeyError:
        if var == -0.0:
            iteration = 1
            varDict[iteration - 1].append(var)
    return iteration - 1
    
empiricalArray = np.zeros((9, 9))
#initializes what will become, once the columns are normalized, a right markov matrix of zeros that will contain transition probabilities. the (i, j)th entry of this matrix contains the number of transitions from i providers to j providers.
print totals[7]
for (xinit,xprime) in sorted(empiricalTransitions.keys()):
    if xinit < 9 and xprime < 9:
        print empiricalTransitions[(xinit, xprime)]
        print (xinit, xprime)
        empiricalArray[xprime , xinit] = empiricalTransitions[(xinit, xprime)]
        
print empiricalArray
print totals[7]


empiricalArrayMarkov = normalize(empiricalArray, norm='l1', axis=0)
#normalize the matrix's columns so they all sum to 1 (this makes the matrix a right markov matrix; when you multiply a column vector that is a probability distribution x also summing to 1, the product is the distribution for x stepped forward one interval in time.) for more information try http://www.math.harvard.edu/~knill/teaching/math19b_2011/handouts/lecture33.pdf.
#generally, a markov matrix (also called a stochastic matrix), can be used to express the transition probabilities between states of a markov chain [1]. here the states are the number of broadband providers, and the time steps are the stages the chain goes through.

#[1] a markov chain represents the evolution of a random variable over time. at time = 0 we know its state; the markov matrix represents the transition between states at time steps. take a look at http://en.wikipedia.org/wiki/Markov_chain. markov matrices have steady states that are the solution to the equation Ax = x (alternatively the eigenvector for lambda = 1) where A is a markov matrix and x is a column vector. as time goes to infinity, the state of the markov chain approaches the steady state vector. all markov matrices are guaranteed to have such a steady state. see also http://en.wikipedia.org/wiki/Stochastic_matrix.
print np.sum(empiricalArrayMarkov, axis = 0)
print empiricalArrayMarkov

#for each bin (r, g, h) corresponding to different ranges of values of population density, gini index, and entropy of race distributions, we calculate a markov matrix from the available data as we just did for the empirical array (which is a nationally representative transition model)
conditionalProbs = {}
for binned in conditionalTransitions.keys():
    conditionalProbs[binned] = {}
    condMarkov = np.zeros((9, 9))
    for (xinit, xprime) in conditionalTransitions[binned].keys():
        if xinit < 9 and xprime < 9:
            condMarkov[xprime, xinit] = conditionalTransitions[binned][(xinit, xprime)]
    conditionalProbs[binned]['markov'] = normalize(condMarkov, norm = 'l1', axis = 0)
    #conditionalProbs[binned]['steady state'] = eigenvector for lambda = 1
#print hasBroadband.keys()
print hasBroadband['50019']
#here is the user interaction part. for a given county code, it gives the average and distribution of number of broadband providers in dec. 2012 and steps forward 4 time steps (2 years) to dec. 2014 to estimate current distributions and averages based on both national data (empiricalArray) and data from counties that have the same binned (pop density, gini index, entropy of racial distribution). 
stop = False
while stop == False:
    county = raw_input('type county code')
    print 'in dec 2012, the distribution was'
    print hasBroadband[county]['dec2012']
    print 'and the average was'
    totally = 0.0
    iterator = 0.0
    for key in hasBroadband[county]['dec2012'].keys():
        totally += iterator * hasBroadband[county]['dec2012'][key]
        iterator += 1.0
    print float(totally)
    print 'based on national averages, the current distribution is'
    (rho, gini, entropy) = countyDemog[str(county)]
    r = gaussian_bin_var(np.log2(rho), rhoMean, rhoSigma, rhoDict)
    g = gaussian_bin_var(gini, giniMean, giniSigma, giniDict)
    h = sketchy_bin_var(entropy, entropyStep, entropyMax, entropyDict)
    binned = (r, g, h)
    initState = np.zeros(9)
    index = 0
    for key in sorted(hasBroadband[county]['dec2012'].keys()):
        initState[index] += hasBroadband[county]['dec2012'][key]
    
    print (np.linalg.matrix_power(empiricalArrayMarkov, 4)).dot(initState)
    print 'and its average will be'
    foo = 0.0
    iterator = 0.0
    for y in (np.linalg.matrix_power(empiricalArrayMarkov, 4)).dot(initState):
        foo += y * iterator
        iterator += 1.0
    print foo
    print 'based on statistics from communities like it, the current distribution is'
    #print np.shape(conditionalProbs[binned]['markov'])
    print (np.linalg.matrix_power(conditionalProbs[binned]['markov'], 4)).dot(initState)
    print 'and its average will be'
    foo = 0.0
    iterator = 0.0
    for y in (np.linalg.matrix_power(conditionalProbs[binned]['markov'], 4)).dot(initState):
        foo += y * iterator
        iterator += 1.0
    print foo
    if raw_input('to continue press y') != 'y':
        stop = True
    