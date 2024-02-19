import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import random
from var import *

# Player -> Creature
# Prey -> Animal -> Creature
# Predator -> Animal -> Creature
 
class Creature(pygame.sprite.Sprite):
    def __init__(self, color, size, speed):
        # attributes
        self.color = color
        self.speed = speed*PLAY_SPEED_MOD
        self.size = size
        # create sprite
        super(Creature, self).__init__()

class Animal(Creature):
    def __init__(self, color, size, speed, sense):
        super(Animal, self).__init__(color, size, speed)
        self.sense = sense

class Player(Creature):
    def __init__(self, color, size, speed):
        super(Player, self).__init__(color, size, speed)
        self.surf = pygame.Surface((self.size, self.size*1.5))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys):
        # move player
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1*self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1*self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1*self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1*self.speed, 0)
        # keep in bounds
        if self.rect.left < BUFFER/2:
            self.rect.left = BUFFER/2
        if self.rect.right > SCREEN_WIDTH-BUFFER/2:
            self.rect.right = SCREEN_WIDTH-BUFFER/2
        if self.rect.top <= BUFFER/2 - self.size:
            self.rect.top = BUFFER/2 - self.size
        if self.rect.bottom >= SCREEN_HEIGHT-BUFFER/2:
            self.rect.bottom = SCREEN_HEIGHT-BUFFER/2

class Prey(Animal):
    def __init__(self, color, size, speed, sense):
        super(Prey, self).__init__(color, size, speed, sense)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0+BUFFER, SCREEN_WIDTH-BUFFER),
                random.randint(0+BUFFER, SCREEN_HEIGHT-BUFFER),
            )
        )
        self.prev_move_x = 0
        self.prev_move_y = 0
    def update(self):
        # apply movement based on prior frame
        if self.prev_move_x == -1:
            move_x = random.choices([-1,0,1],[0.9,0.09,0.01])[0]
        if self.prev_move_x == 0:
            move_x = random.randint(-1, 1)
        if self.prev_move_x == 1:
            move_x = random.choices([-1,0,1],[0.01,0.09,0.9])[0]
        if self.prev_move_y == -1:
            move_y = random.choices([-1,0,1],[0.9,0.09,0.01])[0]
        if self.prev_move_y == 0:
            move_y = random.randint(-1, 1)
        if self.prev_move_y == 1:
            move_y = random.choices([-1,0,1],[0.01,0.09,0.9])[0]
        # move_x = random.randint(-1, 1)
        # move_y = random.randint(-1, 1)
        self.rect.move_ip(move_x*self.speed, move_y*self.speed)
        # save movement for next frame
        self.prev_move_x = move_x
        self.prev_move_y = move_y

class Plant(pygame.sprite.Sprite):
    def __init__(self, color, size, age, growth, berries):
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
        elif self.size >= PLANT_SIZE_MAX and self.age > self.next_growth and self.berries < PLANT_BERRIES_MAX:
            self.add_berry()
            self.berries += 1
            self.draw()
            self.next_growth += PLANT_GROWTH_INTERVAL

class Berry(pygame.sprite.Sprite):
    def __init__(self, color, size, plant):
        self.color = color
        self.size = size
        self.plant = plant
        # create sprite
        super(Berry, self).__init__()
        # draw
        self.draw()
        print(plant.rect.x,plant.rect.x+size*2)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(plant.rect.x, plant.rect.x+plant.size*2),
                random.randint(plant.rect.y, plant.rect.y+plant.size*2),
            )
        )
    def draw(self):
        self.surf = pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size, self.size)
    def update(self):
        self.draw()