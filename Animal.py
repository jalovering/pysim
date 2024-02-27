import pygame
from Creature import Creature
from var import *

class Animal(Creature):
    def __init__(self, color, size, speed, status, statusLastUpdated, sense):
        super(Animal, self).__init__(color, size, speed, status, statusLastUpdated)
        self.sense = sense
        self.sensePlayer = False
        self.sensePlayerLoc = ()
        self.senseFood = False
        self.senseFoodLoc = ()
        self.touchFood = False
        self.touchFoodSource = "n/a"
    def create_sensor(self):
        add_sensor_event = pygame.event.Event(ADDSENSOR, animal=self)
        pygame.event.post(add_sensor_event)