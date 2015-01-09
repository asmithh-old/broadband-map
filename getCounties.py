          
          

while keepGoing:
    entropy = raw_input ('what is race entropy?') 
    rho = raw_input('what is population density?')      
    gini = raw_input('what is gini index?')
    r = 0
    h = 0
    g = 0
    while rho < max(rdivided[r]):
        r += 1
    while entropy < max(hdivided[h]):
        h += 1
    while gini < max(gdivided[g]):
        g += 1
    print conditional[(r, h, g)]
    stop = raw_input('if you want to stop, type "stop"')
    if stop == "stop":
        keepGoing = False
    