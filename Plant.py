import pygame
import random
from var import *

class Plant(pygame.sprite.Sprite):
    def __init__(self, color=COLOR_PLANT, size=4, age=1, growth=1, berries=[]):
        self.color = color
        self.size = size
        self.age = age
        self.growth = growth
        self.berries = berries
        # create sprite
        super(Plant, self).__init__()
        # draw
        self.draw()
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0+BUFFER, SCREEN_WIDTH-BUFFER),
                random.randint(0+BUFFER, SCREEN_HEIGHT-BUFFER),
            )
        )
        self.next_growth = PLANT_GROWTH_INTERVAL
    def draw(self):
        self.surf = pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size, self.size)
    def add_berry(self):
        add_berry_event = pygame.event.Event(ADDBERRY, plant=self)
        pygame.event.post(add_berry_event)
    def update(self):
        # age in frames
        self.age += 1*PLAY_SPEED_MOD
        # size
        if self.size < PLANT_SIZE_MAX and self.age > self.next_growth: 
            self.size += 1 * self.growth
            self.draw()
            self.next_growth += PLANT_GROWTH_INTERVAL
        elif self.size >= PLANT_SIZE_MAX and self.age > self.next_growth and len(self.berries) < PLANT_BERRIES_MAX:
            self.add_berry()
            self.draw()
            self.next_growth += PLANT_GROWTH_INTERVAL