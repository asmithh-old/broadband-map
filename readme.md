#for broadbandmap.py:

okay, so there's all this code here. basically what all this code does is take demographic data and broadband availability data from broadbandmap.gov and finds the empirical distribution [1] of percent of households with broadband internet [2] given the following demographic metrics: racial diversity [3]; economic diversity [4]; and population density [5]. 

[1]: an empirical distribution is a probability distribution drawn from a data set. it's our estimate of the probability distribution the data comes from based strictly on the data.  for example, to get the empirical probability of event x, we look at the number of times event x happens and divide it by the total number of events.  as the number of data points approaches infinity, the empirical distribution approaches the actual distribution. for a mathematically rigorous explanation of this, check out the wikipedia article on the weak law of large numbers. 

[2] broadband internet here defined as download speed greater than 3mbps (this is how the broadband.gov api returns it); the current FCC definition of broadband access is 4 mbps so this is not an entirely accurate metric, but it's the best balance of convenience and accuracy available.

[3] racial diversity measured as the shannon entropy of the distribution of races. maximum entropy is achieved with an even distribution of races, and minimum entropy (0) achieved with 100% of the population one race. the shannon entropy (again, check out the wikipedia page) is mathematically the negative of the sum (over all events x ) of the probability of x times the log base 2 of the probability of x and intuitively how surprised you are, on average, by a sample drawn from the distribution. entropy is a measure of information. entropy with log base 2 is measured in bits (which is how the size of files is measured); entropy with log base e is measured in nats which is a funny name for a unit.

[4] economic diversity is measured by the gini index, with perfect equality (everyone earns the same amount) at 0 and perfect inequality (one person earns all the money) at 1.0.  mathematically, it is 1.0 minus the ratio of [the area under the curve where y is the percent of the community's total income cumulatively earned by the bottom x% of earners] to [the area under the line of perfect equality which has slope 1--everyone earns the same].  the wikipedia article has a picture that explains it a lot better than i can. this follows a Gaussian (normal) distribution with mean approximately .43

[5] population density is the number of people per square kilometer. interestingly, the log of population density also follows a Gaussian (normal) distribution. 

you can input a county code or a tuple of (population density, racial entropy, economic diversity) to return the empirical distribution for broadband access in areas with similar population density, racial entropy, and economic diversity.
this will be in the form of [for n in [0:10], the probability for a community with these characteristics, approximately (n * 10)% of its population will have broadband access]

#to run:
try:

- 02261: Valdez-Cordova Census Area, Alaska
- 06041: Marin County, California
- 44007: Providence County, Rhode Island (RI is the most population-dense state in the US)
- 74300: Midway Islands
