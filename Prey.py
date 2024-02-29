import pygame
from Animal import Animal
from var import *
import random

class Prey(Animal):
    def __init__(self, color=COLOR_PREY, size=10, speed=1, status="moving", statusLastUpdated=0, hunger=0, age=0, sense=100, sensor=None):
        super(Prey, self).__init__(color, size, speed, status, statusLastUpdated, hunger, age, sense, sensor)
        self.surf = pygame.Surface((self.size*1.5, self.size))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0+BUFFER, SCREEN_WIDTH-BUFFER),
                random.randint(0+BUFFER, SCREEN_HEIGHT-BUFFER),
            )
        )
        self.text_font_hunger = pygame.font.Font(None, 16)
        self.text_surf = self.text_font_hunger.render(str(self.hunger), True, (0,0,0))
        self.create_sensor()
        self.prev_move_x = 0
        self.prev_move_y = 0
        self.next_hunger = PREY_HUNGER_INTERVAL
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
    def start_eat(self):
        # update status
        self.status = "eating"
        self.statusLastUpdated = pygame.time.get_ticks()
    def finish_eat(self):
        # remove berry
        random_berry = random.choice(self.touchFoodSource.berries)
        self.touchFoodSource.berries.remove(random_berry)
        random_berry.kill()
        del random_berry
        # update status
        self.status = "moving"
        self.statusLastUpdated = pygame.time.get_ticks()
        # update hunger
        self.hunger -= 1
        self.update_hunger_text()
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
    def update_hunger_text(self):
        self.text_surf = self.text_font_hunger.render(str(self.hunger), True, (0,0,0))
    def start_dying(self):
        print("dying")
        self.status = "dying"
        self.statusLastUpdated = pygame.time.get_ticks()
    def die(self):
        print("died")
        self.sensor.kill()
        del self.sensor
        self.kill()
        del self
    def update(self,plant_group):
        ## GUARANTEED UPDATES ##
        if self.status == "dying" and (self.statusLastUpdated + (PREY_DYING_TIME/PLAY_SPEED_MOD)) >= pygame.time.get_ticks():
            move_x, move_y = 0,0
            sensor_color_list = list(self.sensor.color)
            sensor_color_list[3] -= 1
            sensor_color_list[3] = max(sensor_color_list[3], 0)
            self.sensor.color = tuple(sensor_color_list)
            self.sensor.draw()
            return
        elif self.status == "dying" and (self.statusLastUpdated + (PREY_DYING_TIME/PLAY_SPEED_MOD)) < pygame.time.get_ticks():
            self.die()
            return
        # age in frames
        self.age += 1*PLAY_SPEED_MOD
        # hunger
        if self.age > self.next_hunger: 
            self.hunger += 1
            self.next_hunger += PREY_HUNGER_INTERVAL
            self.update_hunger_text()
        if self.hunger >= PREY_DEATH_BY_HUNGER:
            self.start_dying()
        ## CONDITIONAL UPDATES ##
        # check colissions
        self.touch_plant(plant_group)
        if self.sensePlayer:
            move_x, move_y = self.move_away()
            self.status = "moving"
            self.statusLastUpdated = pygame.time.get_ticks()
        elif self.touchFood:
            if self.status == "eating" and (self.statusLastUpdated + (PREY_EAT_TIME/PLAY_SPEED_MOD)) >= pygame.time.get_ticks() :
                move_x, move_y = 0,0
                exit
            elif self.status == "eating" and (self.statusLastUpdated + (PREY_EAT_TIME/PLAY_SPEED_MOD)) < pygame.time.get_ticks():
                self.finish_eat()
                move_x, move_y = self.move_random()
                exit
            else:
                self.start_eat()
                move_x, move_y = 0,0
                exit
        elif self.senseFood:
            # print("SENSE FOOD")
            move_x, move_y = self.move_toward()
        else:
            move_x, move_y = self.move_random()
        ## MOVEMENT ##
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