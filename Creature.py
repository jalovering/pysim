import pygame
from var import *

class Creature(pygame.sprite.Sprite):
    def __init__(self, color, size, speed, status, statusLastUpdated):
        # attributes
        self.color = color
        self.speed = speed*PLAY_SPEED_MOD
        self.size = size
        self.status = status
        self.statusLastUpdated = statusLastUpdated
        # create sprite
        super(Creature, self).__init__()