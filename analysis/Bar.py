import pygame
from var import *

class Bar(pygame.sprite.Sprite):
    def __init__(self, color, x, y, height, width):
        # properties
        self.color = color
        self.initialColor = color
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        # create sprite
        super(Bar, self).__init__()
        # create bar
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(x=self.x, y=self.y)
    def hoverOn(self):
        # change properties
        self.color = (225,225,225)
        self.x -= 1
        self.y -= 1
        self.height += 2
        self.width += 2
        # apply properties
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(x=self.x, y=self.y)