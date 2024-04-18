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
    if gene == "speed":
        numValues = (maxValue-minValue)*10^decimals / 2
    if gene == "sense":
        numValues = (maxValue-minValue)*10^decimals / 10
    
    dist = {}
    for value in range(minValue,maxValue):
        dist[value] = 0
    for value in arr:
        dist[value] +=  1
    return dist

    # dist = np.zeros((numValues, 2))
    # for val in range(minValue,maxValue):
    # for value in arr:
    #     if value in dist:
    #         dist[value] +=  1
    #     else:
    #         dist[value] = 1
    # return dist