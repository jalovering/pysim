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
from classes import *
from var import *

# initialize pygame
pygame.init()

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
surface = pygame.Surface((SCREEN_WIDTH-BUFFER, SCREEN_HEIGHT-BUFFER))
pygame.display.set_caption('pysim') 

# custom event - add prey
# ADDPREY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPREY, int(5000/PLAY_SPEED_MOD))

# custom event - add plant
# ADDPLANT = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLANT, int(6000/PLAY_SPEED_MOD))

# custom event - add berry
# ADDBERRY = pygame.USEREVENT + 3

# sprite groups
prey_group = pygame.sprite.Group()
plant_group = pygame.sprite.Group()
berry_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()

# player object
player = Player(COLOR_PLAYER,20,2)
all_group.add(player)

# initial prey object
new_prey = Prey(COLOR_PREY,20,1,1)
prey_group.add(new_prey)
all_group.add(new_prey)

# initial plant object
new_plant = Plant(COLOR_PLANT,4,1,1,0)
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
            new_prey = Prey(COLOR_PREY,20,1,1)
            prey_group.add(new_prey)
            all_group.add(new_prey)
        # add new plant
        # elif event.type == ADDPLANT:
        #     new_plant = Plant(COLOR_PLANT,4,1,1,0)
        #     plant_group.add(new_plant)
        #     all_group.add(new_plant)
        # add new berry
        elif event.type == ADDBERRY:
            new_berry = Berry(COLOR_BERRY,1,event.plant)
            berry_group.add(new_berry)
            all_group.add(new_berry)

    # user input
    pressed_keys = pygame.key.get_pressed()

    # update player location
    player.update(pressed_keys)

    # update prey locations
    prey_group.update()

    # update plant locations
    plant_group.update()

    # update berry locations
    berry_group.update()

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
    for entity in all_group:
        screen.blit(entity.surf, entity.rect)

    # update display
    pygame.display.flip()
    # print(pygame.time.get_ticks())
    clock.tick(60)