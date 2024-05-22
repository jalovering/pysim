import pygame
from var import *
from analysis.analyze import round_genes

class Bar(pygame.sprite.Sprite):
    def __init__(self, color, x, y, height, width, groupedValue, gene):
        # properties
        self.color = color
        self.initialColor = color
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.groupedValue = groupedValue
        self.gene = gene
        # create sprite
        super(Bar, self).__init__()
        # create bar
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(x=self.x, y=self.y)
    def hoverOn(self,prey_group):
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
        # highlight relevant Animals
        for prey in prey_group:
            if str(round_genes(self.gene,getattr(prey, self.gene))) == self.groupedValue:
                prey.highlightOn()
        