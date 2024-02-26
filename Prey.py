import pygame
from Animal import Animal
from var import *
import random

class Prey(Animal):
    def __init__(self, color=COLOR_PREY, size=10, speed=1, sense=100):
        super(Prey, self).__init__(color, size, speed, sense)
        self.surf = pygame.Surface((self.size*1.5, self.size))
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
    def touch_plant(self, plant_group):
        food_touched = pygame.sprite.spritecollide(self, plant_group, False)
        self.touchFood = False
        if food_touched == []:
            return False
        for plant in food_touched:
            if len(plant.berries) >= 1:
                self.touchFood = True
                self.touchFoodSource = plant
                return True
        return False
    def eat_berry(self):
        random_berry = random.choice(self.touchFoodSource.berries)
        self.touchFoodSource.berries.remove(random_berry)
        random_berry.kill()
        # del random_berry
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
        self.touch_plant(plant_group)
        if self.sensePlayer:
            # print("SENSE PLAYER")
            move_x, move_y = self.move_away()
        elif self.touchFood:
            move_x, move_y = 0,0
            self.eat_berry()
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
        if self.rect.top <= BUFFER/2:
            self.rect.top = BUFFER/2
        if self.rect.bottom >= SCREEN_HEIGHT-BUFFER/2:
            self.rect.bottom = SCREEN_HEIGHT-BUFFER/2
        # save movement for next frame
        self.prev_move_x = move_x
        self.prev_move_y = move_y