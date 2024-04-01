import pygame
from pygame.locals import *
from Player import Player
from Plant import Plant
from Prey import Prey
from Sensor import Sensor
from Berry import Berry
from var import *
import random
import sidebar

# initialize pygame
pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
surface = pygame.Surface((SURFACE_MAIN_WIDTH, SCREEN_HEIGHT-(BUFFER*2)))
surface_sidebar = pygame.Surface((SURFACE_SIDEBAR_WIDTH, SCREEN_HEIGHT-(BUFFER*2)))
pygame.display.set_caption('pysim') 

# # custom event - add prey
# ADDPREY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDPREY, int(40000/PLAY_SPEED_MOD))

# custom event - add plant
ADDPLANT = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLANT, int(240000/PLAY_SPEED_MOD))

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
for i in range(8):
    new_prey = Prey(color=(1,1,1))
    prey_group.add(new_prey)
    all_group.add(new_prey)

# for i in range(1):
#     new_prey = Prey(color=(1,1,1),size=15)
#     prey_group.add(new_prey)
#     all_group.add(new_prey)

# initial plant object
for i in range(10):
    new_plant = Plant(size=random.randint(1,10))
    plant_group.add(new_plant)
    all_group.add(new_plant)

# sidebar
start_index = 0

# game loop
clock = pygame.time.Clock()
running = True
while running: 

    # event handler
    for event in pygame.event.get(): 
        # QUIT - window close      
        if event.type == pygame.QUIT: 
            running = False
        # sidebar scroll
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4:  # scroll up
                start_index = sidebar.scroll(-SIDEBAR_SCROLL_SPEED, prey_group.sprites(), start_index)
            elif event.button == 5:  # scroll down
                start_index = sidebar.scroll(SIDEBAR_SCROLL_SPEED, prey_group.sprites(), start_index)
        # add new prey
        elif event.type == ADDPREY:
            new_prey = Prey()
            prey_group.add(new_prey)
            all_group.add(new_prey)
        # add new baby prey
        elif event.type == ADDPREYBABY:
            new_prey = Prey(
                parent=event.parent
                )
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
    surface_sidebar.fill(COLOR_SURFACE_SIDEBAR)
    screen.blit(surface,(BUFFER,BUFFER))
    screen.blit(surface_sidebar,((BUFFER*2)+SURFACE_MAIN_WIDTH,BUFFER))

    # draw sprites
    for entity in sensor_group:
        screen.blit(entity.surf, entity.rect)
    for entity in prey_group:
        screen.blit(entity.surf, entity.rect)
        screen.blit(entity.text_surf, (entity.rect.x + 50, entity.rect.y + 10))
    for entity in plant_group:
        screen.blit(entity.surf, entity.rect)
    for entity in berry_group:
        screen.blit(entity.surf, entity.rect)
    screen.blit(player.surf, player.rect)

    # draw sidebar
    sidebar.write_sidebar(screen, prey_group.sprites(), start_index)

    ### TESTING START
    # print(pygame.time.get_ticks())
    # print(plant_group)
    ### TESTING END

    # update display
    pygame.display.flip()
    clock.tick(FPS)