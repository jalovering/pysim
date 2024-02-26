import pygame
from var import *

class Sensor(pygame.sprite.Sprite):
    def __init__(self, animal, color=COLOR_SENSOR, size=100):
        self.animal = animal
        self.color = color
        self.size = size
        # create sprite
        super(Sensor, self).__init__()
        # draw
        self.draw()
        self.rect = self.surf.get_rect(center=(self.animal.rect.x, self.animal.rect.y))
    def draw(self):
        self.surf = pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size, self.size)
    def update(self,player,plant_group):
        self.sense_player(player)
        self.sense_food(plant_group)
        self.rect.center = self.animal.rect.center
    def sense_player(self, player):
        colissions = pygame.sprite.spritecollide(self, pygame.sprite.GroupSingle(player), False)
        if colissions == []:
            self.animal.sensePlayer = False
            return False
        else:
            self.animal.sensePlayer = True
            # self.animal.sensePlayerLoc = (player.rect.x,player.rect.y)
            self.animal.sensePlayerLoc = player.rect.center
            return True
    def sense_food(self, plant_group):
        food_sensed = pygame.sprite.spritecollide(self, plant_group, False)
        self.animal.senseFood = False
        if food_sensed == []:
            return False
        for plant in food_sensed:
            if len(plant.berries) >= 1:
                self.animal.senseFood = True
                self.animal.senseFoodLoc = plant.rect.center
                return True
        return False