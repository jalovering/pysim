import numpy as np

def create_prey_stats(prey_sprites):
    num_prey = len(prey_sprites)
    prey_stats = np.zeros((num_prey, 3))

    for i, prey in enumerate(prey_sprites):
        prey_stats[i] = [prey.size, prey.speed, prey.sense]

    return prey_stats