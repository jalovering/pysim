import pygame
### CONSTANTS ###
## color
# Tol Colorblind Palette
c1 = (51,34,136) #332288
c2 = (17,119,51) #117733
c3 = (68,170,153) #44AA99
c4 = (136,204,238) #88CCEE
c5 = (221,204,119) #DDCC77
c6 = (204,102,119) #CC6677
c7 = (170,68,153) #AA4499
c8 = (136,34,85) #882255
COLOR_BG = (118,133,136)
COLOR_SURFACE = (147,168,171)
COLOR_PREY = (106,116,158)
COLOR_PLANT = (112, 156, 124)
COLOR_BERRY = (194, 114, 118)
COLOR_PLAYER = (158, 116, 106)
COLOR_SENSOR = (175, 175, 175, 200)
# COLOR_BG = c5
# COLOR_SURFACE = c3
# COLOR_PREY = (106,116,158)
# COLOR_PLANT = c2
# COLOR_BERRY = c8
# COLOR_PLAYER = (158, 116, 106)
# COLOR_SENSOR = c5
## screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BUFFER = 60
## time
PLAY_SPEED_MOD = 6
PLAY_SPEED_MOD = 1
## genes
PREY_EAT_TIME = 1000 # takes 1000ms to eat
PREY_HUNGER_INTERVAL = 600 # gain 1 hunger every 600 frames (10 seconds)
PREY_DYING_TIME = 3000 # takes 1000ms to die
PLANT_GROWTH_INTERVAL = 600 # grow every 600 frames (10 seconds)
PLANT_SIZE_MAX = 10
PLANT_BERRIES_MAX = 10
## custom events
ADDPREY = pygame.USEREVENT + 1
ADDPLANT = pygame.USEREVENT + 2
ADDBERRY = pygame.USEREVENT + 3
ADDSENSOR = pygame.USEREVENT + 4