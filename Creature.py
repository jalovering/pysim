import pygame
from var import *

class Creature(pygame.sprite.Sprite):
    def __init__(self, color, size, speed):
        # attributes
        self.color = color
        self.speed = speed*PLAY_SPEED_MOD
        self.size = size
        # create sprite
        super(Creature, self).__init__()