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
import math

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

class Player(Creature):
    def __init__(self, color=COLOR_PLAYER, size=20, speed=2):
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

class Animal(Creature):
    def __init__(self, color, size, speed, sense):
        super(Animal, self).__init__(color, size, speed)
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

class Prey(Animal):
    def __init__(self, color=COLOR_PREY, size=20, speed=1, sense=100):
        super(Prey, self).__init__(color, size, speed, sense)
        self.surf = pygame.Surface((self.size, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0+BUFFER, SCREEN_WIDTH-BUFFER),
                random.randint(0+BUFFER, SCREEN_HEIGHT-BUFFER),
            )
        )
        self.create_sensor()
        self.prev_move_x = 0
        self.prev_move_y = 0
    def touch_food(self, plant_group):
        food_sensed = pygame.sprite.spritecollide(self, plant_group, False)
        self.touchFood = False
        if food_sensed == []:
            return False
        for plant in food_sensed:
            if plant.berries >= 1:
                self.touchFood = True
                self.touchFoodSource = plant.rect.center
                return True
        return False
    def move_random(self):
        # apply movement based on prior frame
        if self.prev_move_x == -1:
            move_x = random.choices([-1,0,1],[0.95,0.04,0.01])[0]
        if self.prev_move_x == 0:
            move_x = random.randint(-1, 1)
        if self.prev_move_x == 1:
            move_x = random.choices([-1,0,1],[0.01,0.04,0.95])[0]
        if self.prev_move_y == -1:
            move_y = random.choices([-1,0,1],[0.95,0.04,0.01])[0]
        if self.prev_move_y == 0:
            move_y = random.randint(-1, 1)
        if self.prev_move_y == 1:
            move_y = random.choices([-1,0,1],[0.01,0.04,0.95])[0]
        return move_x, move_y
    def move_away(self):
        diff_x = self.rect.center[0] - self.sensePlayerLoc[0]
        diff_y = self.rect.center[1] - self.sensePlayerLoc[1]
        if(diff_x > 0):
            move_x = 1
        elif(diff_x < 0):
            move_x = -1
        else:
            move_x = 0
        if(diff_y > 0):
            move_y = 1
        elif(diff_y < 0):
            move_y = -1
        else:
            move_y = 0
        return move_x, move_y
    def move_toward(self):
        diff_x = self.rect.center[0] - self.senseFoodLoc[0]
        diff_y = self.rect.center[1] - self.senseFoodLoc[1]
        if(diff_x > 0):
            move_x = -1
        elif(diff_x < 0):
            move_x = 1
        else:
            move_x = 0
        if(diff_y > 0):
            move_y = -1
        elif(diff_y < 0):
            move_y = 1
        else:
            move_y = 0
        return move_x, move_y
    def update(self,plant_group):
        self.touch_food(plant_group)
        if self.sensePlayer:
            # print("SENSE PLAYER")
            move_x, move_y = self.move_away()
        elif self.touchFood:
            move_x, move_y = 0,0
            exit
        elif self.senseFood:
            # print("SENSE FOOD")
            move_x, move_y = self.move_toward()
        else:
            move_x, move_y = self.move_random()
        # move_x = random.randint(-1, 1)
        # move_y = random.randint(-1, 1)
        self.rect.move_ip(move_x*self.speed, move_y*self.speed)
        # keep in bounds
        if self.rect.left < BUFFER/2:
            self.rect.left = BUFFER/2
        if self.rect.right > SCREEN_WIDTH-BUFFER/2:
            self.rect.right = SCREEN_WIDTH-BUFFER/2
        if self.rect.top <= BUFFER/2 - self.size:
            self.rect.top = BUFFER/2 - self.size
        if self.rect.bottom >= SCREEN_HEIGHT-BUFFER/2:
            self.rect.bottom = SCREEN_HEIGHT-BUFFER/2
        # save movement for next frame
        self.prev_move_x = move_x
        self.prev_move_y = move_y

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
            if plant.berries >= 1:
                self.animal.senseFood = True
                self.animal.senseFoodLoc = plant.rect.center
                return True
        return False

class Plant(pygame.sprite.Sprite):
    def __init__(self, color=COLOR_PLANT, size=4, age=1, growth=1, berries=0):
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
    def __init__(self, plant, color=COLOR_BERRY, size=1):
        self.plant = plant
        self.color = color
        self.size = size
        # create sprite
        super(Berry, self).__init__()
        # draw
        self.draw()
        self.place_berry()
    def place_berry(self):
        # Thanks to aioobe's equation here
        # https://stackoverflow.com/questions/5837572/generate-a-random-point-within-a-circle-uniformly
        radius = self.plant.size
        centerX = self.plant.rect.x + radius
        centerY = self.plant.rect.y + radius
        r = radius * math.sqrt(random.uniform(0,1))
        theta = random.uniform(0,1) * 2 * math.pi
        x = int(centerX + r * math.cos(theta))
        y = int(centerY + r * math.sin(theta))
        self.rect = self.surf.get_rect(center=(x,y))
    def draw(self):
        self.surf = pygame.Surface((self.size*2,self.size*2),pygame.SRCALPHA)
        pygame.draw.circle(self.surf, self.color, (self.size, self.size), self.size, self.size)
    def update(self):
        self.draw()