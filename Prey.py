import pygame
from Animal import Animal
from var import *
import random

class Prey(Animal):
    def __init__(self, color=COLOR_PREY, size=10, speed=1, status="moving", statusLastUpdated=0, hunger=10, age=0, sense=100, sensor=None, birthLoc=()):
        super(Prey, self).__init__(color, size, speed, status, statusLastUpdated, hunger, age, sense, sensor, birthLoc)
        self.surf = pygame.Surface((self.size*1.5, self.size))
        self.surf.fill(self.color)
        if birthLoc == ():
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(0+BUFFER, SCREEN_WIDTH-BUFFER),
                    random.randint(0+BUFFER, SCREEN_HEIGHT-BUFFER),
                )
            )
        else:
            self.rect = self.surf.get_rect(center=birthLoc)
        self.text_font_hunger = pygame.font.Font(None, 16)
        self.text_surf = self.text_font_hunger.render(str(self.hunger), True, (0,0,0))
        self.create_sensor()
        self.prev_move_x = 0
        self.prev_move_y = 0
        self.next_hunger = PREY_HUNGER_INTERVAL
        self.next_mate = PREY_MATE_INTERVAL
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
    def touch_prey(self, prey_group):
        prey_touched = pygame.sprite.spritecollide(self, prey_group, False)
        self.touchFood = False
        if prey_touched == []:
            return False
        for prey in prey_touched:
            if prey.age > prey.next_mate and prey.hunger >= 8:
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
        # remove berry
        random_berry = random.choice(self.touchFoodSource.berries)
        self.touchFoodSource.berries.remove(random_berry)
        random_berry.kill()
        del random_berry
        # update status
        self.status = "moving"
        self.statusLastUpdated = pygame.time.get_ticks()
        # update hunger
        if self.hunger < 10:
            self.hunger += 1
        self.update_hunger_text()
        print("finished eating")
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
        diff_x = self.rect.center[0] - loc[0]
        diff_y = self.rect.center[1] - loc[1]
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
        add_prey_baby_event = pygame.event.Event(ADDPREYBABY, birthLoc=self.rect.center)
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
        # age in frames
        self.age += 1*PLAY_SPEED_MOD
        # hunger
        if self.age > self.next_hunger: 
            self.hunger -= 1
            self.next_hunger += PREY_HUNGER_INTERVAL
            self.update_hunger_text()
        ## STATUS UPDATES ##
        # courting
        if self.age > self.next_mate and self.hunger >= 8:
            self.status = "courting"
        elif self.hunger < 10 and self.status != "eating":
            self.status = "foraging"
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
                self.next_mate += PREY_MATE_INTERVAL
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
                    print(self.status," eating")
                    if (self.statusLastUpdated + (PREY_EAT_TIME/PLAY_SPEED_MOD)) >= pygame.time.get_ticks() :
                        return
                    elif (self.statusLastUpdated + (PREY_EAT_TIME/PLAY_SPEED_MOD)) < pygame.time.get_ticks():
                        print(self.status," finish eating")
                        self.finish_eat()
                        move_x, move_y = self.move_random()
                else:
                    print(self.status," start eating")
                    self.start_eat()
                    return
            elif self.senseFood:
                print(self.status," forage toward")
                move_x, move_y = self.move_toward(self.senseFoodLoc)
            else:
                print(self.status," forage random")
                move_x, move_y = self.move_random()
        # if no collisions, move randomly
        else:
            print(self.status," move random")
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