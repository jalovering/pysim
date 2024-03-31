import pygame
from var import *

class Sensor(pygame.sprite.Sprite):
    def __init__(self, animal, color=COLOR_SENSOR):
        self.animal = animal
        self.color = color
        self.size = self.animal.sense
        # create sprite
        super(Sensor, self).__init__()
        # draw
        self.draw()
        self.rect = self.surf.get_rect(center=(self.animal.rect.x, self.animal.rect.y))
    def draw(self):
        self.surf = pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size, self.size)
    def sense_player(self, player):
        colissions = pygame.sprite.spritecollide(self, pygame.sprite.GroupSingle(player), False)
        if colissions == []:
            self.animal.sensePlayer = False
            return False
        else:
            self.animal.sensePlayer = True
            self.animal.sensePlayerLoc = player.rect.center
            return True
    def sense_food(self, plant_group):
        food_sensed = pygame.sprite.spritecollide(self, plant_group, False)
        self.animal.senseFood = False
        if food_sensed == []:
            return False
        for plant in food_sensed:
            if self.animal.canEatPlant:
                self.animal.senseFood = True
                self.animal.senseFoodLoc = plant.rect.center
                return True
            elif len(plant.berries) >= 1:
                self.animal.senseFood = True
                self.animal.senseFoodLoc = plant.rect.center
                return True
        return False
    def sense_prey(self, prey_group):
        prey_sensed = pygame.sprite.spritecollide(self, prey_group, False)
        self.animal.sensePrey = False
        if prey_sensed == []:
            return False
        for prey in prey_sensed:
            if prey != self.animal and prey.age > prey.next_mate and prey.hunger >= 8:
                self.animal.sensePrey = True
                self.animal.sensePreyLoc = prey.rect.center
                return True
        return False
    def update(self,player,plant_group,prey_group):
        self.sense_player(player)
        if self.animal.status == "courting":
            self.sense_prey(prey_group)
        if self.animal.status == "foraging" and self.animal.senseFood == False:
            self.sense_food(plant_group)
        self.rect.center = self.animal.rect.center
