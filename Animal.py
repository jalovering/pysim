import pygame
from Creature import Creature
from var import *
import numpy as np

class Animal(Creature):
    def __init__(self, color, size, speed, status, statusLastUpdated, hunger, age, sense, sensor, parent):
        super(Animal, self).__init__(color, size, speed, status, statusLastUpdated, hunger, age)
        self.sense = sense
        self.sensor = sensor
        self.parent = parent
        self.sensePlayer = False
        self.sensePlayerLoc = ()
        self.senseFood = False
        self.senseFoodSource = None
        self.touchFood = False
        self.touchFoodSource = None
        self.sensePrey = False
        self.sensePreyLoc = ()
        self.touchPrey = False
        self.touchPreySource = None
    def create_sensor(self):
        add_sensor_event = pygame.event.Event(ADDSENSOR, animal=self)
        pygame.event.post(add_sensor_event)
    def inherit_quantitative_trait(self, trait, parent_value):
        if trait == "size": # int 5-20
            minValue = 5
            maxValue = 20
            scale = 3
            decimals = None
        elif trait == "speed": # float 0.5-5
            minValue = 0.5
            maxValue = 5
            scale = 8
            decimals = 1
        elif trait == "sense": # int 50-300
            minValue = 50
            maxValue = 300
            scale = 1/5
            decimals = None
        # exponential distribution
        lambd = 1 / scale
        mutation = np.random.exponential(scale=lambd)
        if np.random.rand() < 0.5:
            mutation *= -1
        child_value = round(parent_value + mutation, decimals)
        child_value = max(minValue, min(child_value, maxValue))
        return child_value
