import numpy as np

# create array of prey stats
def create_prey_stats(prey_sprites):
    num_prey = len(prey_sprites)
    prey_stats = np.zeros((num_prey, 3))

    for i, prey in enumerate(prey_sprites):
        prey_stats[i] = [prey.size, prey.speed, prey.sense]

    return prey_stats

def create_frequency_dist(arr, gene, minValue, maxValue, decimals):
    if gene == "size":
        numValues = maxValue-minValue
        iteration = 1
    if gene == "speed":
        numValues = (maxValue-minValue)*10**decimals / 2
        iteration = 0.1
    if gene == "sense":
        numValues = (maxValue-minValue) / 10
        iteration = 1
    dist = {}
    tempValue = minValue
    # initialize frequency distribution with zeroes
    while tempValue < maxValue:
        # group values by rounding
        groupedValue = round_genes(gene, tempValue)
        # initialize frequency to zero
        dist[str(groupedValue)] = 0
        # iterate to next possible gene value
        tempValue = round(tempValue + iteration, decimals) # FIX later in Animal.py, stop ints from being floats
    # increment count by 1 for each prey by gene value
    for value in arr:
        value = round(value, decimals)
        groupedValue = round_genes(gene, value) # FIX later in Animal.py, stop ints from being floats
        dist[str(groupedValue)] +=  1
    return dist

def round_genes(gene, value):
# group values accordingly
    if gene == "speed":
        # round to nearest 0.2
        roundedValue = (((value * 10) + 1.5) // 3) * 3
    elif gene == "sense":
        # round to nearest 10
        # roundedValue = ((value + 5) // 10) * 10
        # round to nearest 15
        roundedValue = ((value + 7.5) // 15) * 15
    else:
        roundedValue = value
    return roundedValue
