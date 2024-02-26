import pygame
import random
from var import *
import math

class Berry(pygame.sprite.Sprite):
    def __init__(self, plant, color=COLOR_BERRY, size=1):
        self.plant = plant
        self.color = color
        self.size = size
        # create sprite
        super(Berry, self).__init__()
        # draw
        self.draw()
        self.place_berry()
    def place_berry(self):
        # Thanks to aioobe's equation here
        # https://stackoverflow.com/questions/5837572/generate-a-random-point-within-a-circle-uniformly
        radius = self.plant.size
        centerX = self.plant.rect.x + radius
        centerY = self.plant.rect.y + radius
        r = radius * math.sqrt(random.uniform(0,1))
        theta = random.uniform(0,1) * 2 * math.pi
        x = int(centerX + r * math.cos(theta))
        y = int(centerY + r * math.sin(theta))
        self.rect = self.surf.get_rect(center=(x,y))
    def draw(self):
        self.surf = pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size, self.size)
    def update(self):
        self.draw()