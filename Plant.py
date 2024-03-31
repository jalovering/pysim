import pygame
import random
from var import *

class Plant(pygame.sprite.Sprite):
    def __init__(self, color=COLOR_PLANT, size=4, age=1, growth=1):
        self.color = color
        self.size = size
        self.age = age
        self.growth = growth
        self.berries = []
        # create sprite
        super(Plant, self).__init__()
        # draw
        self.draw()
        self.rect = self.surf.get_rect(
            center=(
                    random.randint(BUFFER, SURFACE_MAIN_WIDTH+BUFFER),
                    random.randint(BUFFER, SCREEN_HEIGHT-BUFFER),
                )
        )
        self.growth_interval = PLANT_GROWTH_INTERVAL / PLAY_SPEED_MOD
        self.next_growth = self.growth_interval
    def draw(self):
        self.surf = pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size, self.size)
    def add_berry(self):
        add_berry_event = pygame.event.Event(ADDBERRY, plant=self)
        pygame.event.post(add_berry_event)
    def update(self):
        # age in ms
        self.age += (1000/FPS)
        # grow (size)
        if self.age > self.next_growth: 
            if self.size < PLANT_SIZE_MAX: 
                self.size += 1 * self.growth
                self.draw()
                self.next_growth += self.growth_interval
            elif self.size >= PLANT_SIZE_MAX and len(self.berries) < PLANT_BERRIES_MAX:
                self.add_berry()
                self.draw()
                self.next_growth += self.growth_interval
            else:
                self.next_growth += self.growth_interval
                return