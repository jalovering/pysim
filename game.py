import pygame
from Player import Player
from Plant import Plant
from Prey import Prey
from Sensor import Sensor
from Berry import Berry
from var import *

# initialize pygame
pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
surface = pygame.Surface((SCREEN_WIDTH-BUFFER, SCREEN_HEIGHT-BUFFER))
pygame.display.set_caption('pysim') 

# # custom event - add prey
# ADDPREY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDPREY, int(40000/PLAY_SPEED_MOD))

# # custom event - add plant
# ADDPLANT = pygame.USEREVENT + 2
# pygame.time.set_timer(ADDPLANT, int(60000/PLAY_SPEED_MOD))

# custom event - add berry
# ADDBERRY = pygame.USEREVENT + 3

# sprite groups
prey_group = pygame.sprite.Group()
sensor_group = pygame.sprite.Group()
plant_group = pygame.sprite.Group()
berry_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()

# player object
player = Player()
all_group.add(player)

# initial prey object
for i in range(2):
    new_prey = Prey(color=(1,1,1))
    prey_group.add(new_prey)
    all_group.add(new_prey)

# initial plant object
for i in range(6):
    new_plant = Plant(size=10)
    plant_group.add(new_plant)
    all_group.add(new_plant)

# game loop
clock = pygame.time.Clock()
running = True
while running: 

    # event handler
    for event in pygame.event.get(): 
        # QUIT - window close      
        if event.type == pygame.QUIT: 
            running = False
        # add new prey
        elif event.type == ADDPREY:
            new_prey = Prey()
            prey_group.add(new_prey)
            all_group.add(new_prey)
        # add new baby prey
        elif event.type == ADDPREYBABY:
            new_prey = Prey(birthLoc=event.birthLoc)
            prey_group.add(new_prey)
            all_group.add(new_prey)
        # add new sensor
        elif event.type == ADDSENSOR:
            new_sensor= Sensor(                
                animal=event.animal,
                )
            event.animal.sensor = new_sensor
            sensor_group.add(new_sensor)
            all_group.add(new_sensor)
        # add new plant
        elif event.type == ADDPLANT:
            new_plant = Plant(
                berries=[]
                )
            plant_group.add(new_plant)
            all_group.add(new_plant)
        # add new berry
        elif event.type == ADDBERRY:
            new_berry = Berry(
                plant=event.plant,
                )
            event.plant.berries.append(new_berry)
            berry_group.add(new_berry)
            all_group.add(new_berry)

    # user input
    pressed_keys = pygame.key.get_pressed()

    # update plant locations
    plant_group.update()

    # update berry locations
    berry_group.update()

    # update prey locations
    sensor_group.update(player,plant_group,prey_group)

    # update prey locations
    prey_group.update(plant_group,prey_group)

    # update player location
    player.update(pressed_keys)

    # reset screen and surface
    screen.fill(COLOR_BG) 
    surface.fill(COLOR_SURFACE)
    screen.blit(
            surface,
            (
                (SCREEN_WIDTH-surface.get_width())/2,
                (SCREEN_HEIGHT-surface.get_height())/2
            )
    )

    # draw sprites
    # for entity in all_group:
    #     screen.blit(entity.surf, entity.rect)
    for entity in sensor_group:
        screen.blit(entity.surf, entity.rect)
    for entity in prey_group:
        screen.blit(entity.surf, entity.rect)
        screen.blit(entity.text_surf, (entity.rect.x + 20, entity.rect.y + 10))
    for entity in plant_group:
        screen.blit(entity.surf, entity.rect)
    for entity in berry_group:
        screen.blit(entity.surf, entity.rect)
    screen.blit(player.surf, player.rect)

    ### TESTING START
    # print(pygame.time.get_ticks())
    ### TESTING END

    # update display
    pygame.display.flip()
    clock.tick(60)