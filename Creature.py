import pygame
from var import *

class Creature(pygame.sprite.Sprite):
    def __init__(self, color, size, speed, status, statusLastUpdated, hunger, age):
        # attributes
        self.color = color
        self.speed = speed
        self.size = size
        self.status = status
        self.statusLastUpdated = statusLastUpdated
        self.hunger = hunger
        self.age = age
        # create sprite
        super(Creature, self).__init__()