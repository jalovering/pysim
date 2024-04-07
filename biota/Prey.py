import pygame
import random
from biota.Animal import Animal
from var import *

class Prey(Animal):
    def __init__(self, color=COLOR_PREY, size=PREY_DEFAULT_SIZE, speed=PREY_DEFAULT_SPEED, status="moving", statusLastUpdated=0, hunger=10, age=0, sense=100, sensor=None, parent=None):
        super(Prey, self).__init__(color, size, speed, status, statusLastUpdated, hunger, age, sense, sensor, parent)
        self.surf = pygame.Surface((self.size*1.5, self.size))
        self.surf.fill(self.color)
        # if there is no parent
        if self.parent == None:
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(BUFFER, SURFACE_MAIN_WIDTH+BUFFER),
                    random.randint(BUFFER, SCREEN_HEIGHT-BUFFER),
                )
            )
        # if there is a parent
        else:
            self.rect = self.surf.get_rect(center=self.parent.rect.center)
            self.size = self.inherit_quantitative_trait("size", self.parent.size)
            self.speed = self.inherit_quantitative_trait("speed", self.parent.speed)
            self.sense = self.inherit_quantitative_trait("sense", self.parent.sense)
        # setup hunger text   
        self.text_font_hunger = pygame.font.Font(None, 16)
        self.text_surf = self.text_font_hunger.render(str(self.hunger), True, (0,0,0))
        # create sensor
        self.create_sensor()
        # set up initial settings
        self.prev_move_x = 0
        self.prev_move_y = 0
        self.hunger_interval = PREY_HUNGER_INTERVAL / ((self.size/PREY_DEFAULT_SIZE)*((self.speed)/PREY_DEFAULT_SPEED)*PLAY_SPEED_MOD)
        self.next_hunger = self.hunger_interval
        self.mate_interval = PREY_MATE_INTERVAL / PLAY_SPEED_MOD
        self.next_mate = self.mate_interval
        self.canEatPlant = self.size >= 15
    def touch_plant(self, plant_group):
        food_touched = pygame.sprite.spritecollide(self, plant_group, False)
        self.touchFood = False
        if food_touched == []:
            return False
        for plant in food_touched:
            if self.canEatPlant:
                self.touchFood = True
                self.touchFoodSource = plant
                return True
            elif len(plant.berries) >= 1:
                self.touchFood = True
                self.touchFoodSource = plant
                return True
        return False
    def touch_prey(self, prey_group):
        prey_touched = pygame.sprite.spritecollide(self, prey_group, False)
        self.touchPrey = False
        if prey_touched == []:
            return False
        for prey in prey_touched:
            if prey != self and prey.age > prey.next_mate and prey.hunger >= 8:
                self.touchPrey = True
                self.touchPreySource = prey
                return True
        return False
    def start_eat(self):
        # update status
        self.status = "eating"
        self.statusLastUpdated = pygame.time.get_ticks()
    def update_hunger_text(self):
        self.text_surf = self.text_font_hunger.render(str(self.hunger), True, (0,0,0))
    def finish_eat(self):
        if len(self.touchFoodSource.berries) >= 1:
            # remove berry
            num_berries = len(self.touchFoodSource.berries)
            random_berry_idx = random.choice(range(num_berries))
            random_berry = self.touchFoodSource.berries[random_berry_idx]
            # kill sprite
            random_berry.kill()
            # delete berry
            del random_berry
            # remove from berry list on host plant
            del self.touchFoodSource.berries[random_berry_idx]
        else:
            self.touchFoodSource.size -= 1
            if self.touchFoodSource.size == 0:
                # kill sprite
                self.touchFoodSource.kill()
                # delete plant
                del self.touchFoodSource
        # update status
        self.status = "moving"
        self.statusLastUpdated = pygame.time.get_ticks()
        self.senseFood = False
        # update hunger
        if self.hunger < 10:
            self.hunger += 1
        self.update_hunger_text()
    def move_random(self):
        # apply movement based on prior frame
        if round(self.prev_move_x) == -1:
            move_x = random.choices([-1,0,1],[0.95,0.04,0.01])[0]
        if round(self.prev_move_x) == 0:
            move_x = random.randint(-1, 1)
        if round(self.prev_move_x) == 1:
            move_x = random.choices([-1,0,1],[0.01,0.04,0.95])[0]
        if round(self.prev_move_y) == -1:
            move_y = random.choices([-1,0,1],[0.95,0.04,0.01])[0]
        if round(self.prev_move_y) == 0:
            move_y = random.randint(-1, 1)
        if round(self.prev_move_y) == 1:
            move_y = random.choices([-1,0,1],[0.01,0.04,0.95])[0]
        return move_x, move_y
    def move_away(self,loc):
        diff_x = self.rect.center[0] - loc[0]
        diff_y = self.rect.center[1] - loc[1]
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
    def move_toward(self,loc):
        diff_x = loc[0] - self.rect.center[0]
        diff_y = loc[1] - self.rect.center[1]
        if diff_x < 0:
            move_x = -1
        elif diff_x > 0:
            move_x = 1
        else:
            move_x = 0
        if diff_y < 0:
            move_y = -1
        elif diff_y > 0:
            move_y = 1
        else:
            move_y = 0
        # correct overshooting when move speed is high
        if (move_x*self.speed*PLAY_SPEED_MOD > diff_x and diff_x > 0) or (move_x*self.speed*PLAY_SPEED_MOD < diff_x and diff_x < 0):
            move_x = round(diff_x/(self.speed*PLAY_SPEED_MOD),2)
        if (move_y*self.speed*PLAY_SPEED_MOD > diff_y and diff_y > 0) or (move_y*self.speed*PLAY_SPEED_MOD < diff_y and diff_y < 0):
            move_y = round(diff_y/(self.speed*PLAY_SPEED_MOD),2)
        return move_x, move_y
    def start_dying(self):
        self.status = "dying"
        self.statusLastUpdated = pygame.time.get_ticks()
    def dying(self):
            sensor_color_list = list(self.sensor.color)
            sensor_color_list[3] -= 1
            sensor_color_list[3] = max(sensor_color_list[3], 0)
            self.sensor.color = tuple(sensor_color_list)
            self.sensor.draw()
    def die(self):
        self.sensor.kill()
        del self.sensor
        self.kill()
        del self
    def birth_baby(self):
        add_prey_baby_event = pygame.event.Event(ADDPREYBABY, parent=self)
        pygame.event.post(add_prey_baby_event)
    def update(self,plant_group,prey_group):
        ## DEATH ##
        if self.hunger <= 0:
            if self.status == "dying" and (self.statusLastUpdated + (PREY_DYING_TIME/PLAY_SPEED_MOD)) >= pygame.time.get_ticks():
                # fade sensor away
                self.dying()
                return
            elif self.status == "dying" and (self.statusLastUpdated + (PREY_DYING_TIME/PLAY_SPEED_MOD)) < pygame.time.get_ticks():
                self.die()
                return
            else:
                self.start_dying()
                return
        ## TIME-BASED UPDATES ##
        # age in ms
        self.age += (1000/FPS)
        # hunger
        if self.age > self.next_hunger: 
            self.hunger -= 1
            self.next_hunger += self.hunger_interval
            self.update_hunger_text()
        ## STATUS UPDATES ##
        # courting
        if self.age > self.next_mate and self.hunger >= 8:
            self.status = "courting"
            self.statusLastUpdated = pygame.time.get_ticks()
        elif self.hunger < 10 and self.status != "eating":
            self.status = "foraging"
            self.statusLastUpdated = pygame.time.get_ticks()
        ## COLLISION-BASED ACTIONS ##
        # player collision
        if self.sensePlayer:
            move_x, move_y = self.move_away(self.sensePlayerLoc)
            self.status = "moving"
            self.statusLastUpdated = pygame.time.get_ticks()
        # prey collision (courting)
        elif self.status == "courting":
            self.touch_prey(prey_group)
            if self.touchPrey:
                if random.choice([0, 1]) == 1:
                    self.birth_baby()
                self.next_mate = self.age + self.mate_interval 
                self.status = "moving"
                move_x, move_y = self.move_random()
            elif self.sensePrey:
                move_x, move_y = self.move_toward(self.sensePreyLoc)
            else:
                move_x, move_y = self.move_random()
        # food collision
        elif self.status == "foraging" or self.status == "eating":
            self.touch_plant(plant_group)
            if self.touchFood:
                if self.status == "eating":
                    if (self.statusLastUpdated + (PREY_EAT_TIME/PLAY_SPEED_MOD)) >= pygame.time.get_ticks() :
                        return
                    elif (self.statusLastUpdated + (PREY_EAT_TIME/PLAY_SPEED_MOD)) < pygame.time.get_ticks():
                        self.finish_eat()
                        move_x, move_y = self.move_random()
                else:
                    self.start_eat()
                    return
            elif self.senseFood:
                if len(self.senseFoodSource.berries) > 0:
                    move_x, move_y = self.move_toward(self.senseFoodSource.rect.center)
                else:
                    self.senseFood = False
                    move_x, move_y = self.move_random()
            else:
                move_x, move_y = self.move_random()
        # if no collisions, move randomly
        else:
            move_x, move_y = self.move_random()
        ## MOVEMENT ##
        self.rect.move_ip(round(move_x*self.speed*PLAY_SPEED_MOD), round(move_y*self.speed*PLAY_SPEED_MOD))
        # keep in bounds
        if self.rect.left < BUFFER:
            self.rect.left = BUFFER
        if self.rect.right > SURFACE_MAIN_WIDTH+BUFFER:
            self.rect.right = SURFACE_MAIN_WIDTH+BUFFER
        if self.rect.top <= BUFFER:
            self.rect.top = BUFFER
        if self.rect.bottom >= SCREEN_HEIGHT-BUFFER:
            self.rect.bottom = SCREEN_HEIGHT-BUFFER
        # save movement for next frame
        self.prev_move_x = move_x
        self.prev_move_y = move_y