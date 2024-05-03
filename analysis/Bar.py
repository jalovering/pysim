import pygame
from var import *

class Bar(pygame.sprite.Sprite):
    def __init__(self, color, x, y, height, width):
        # attributes
        self.color = color
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        # create sprite
        super(Bar, self).__init__()
        # create bar
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(x=x, y=y)