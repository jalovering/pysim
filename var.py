import pygame
### CONSTANTS ###
## color
COLOR_BG = (118,133,136)
COLOR_SURFACE = (147,168,171)
COLOR_PREY = (106,116,158)
COLOR_PLANT = (112, 156, 124)
COLOR_BERRY = (194, 114, 118)
COLOR_PLAYER = (158, 116, 106)
COLOR_SENSOR = (175, 175, 175, 150)
# COLOR_SENSOR = COLOR_BERRY
## screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BUFFER = 60
## time
PLAY_SPEED_MOD = 10
PLAY_SPEED_MOD = 1
## genes
PLANT_GROWTH_INTERVAL = 600 # grow every 10 seconds
PLANT_SIZE_MAX = 10
PLANT_BERRIES_MAX = 10
## custom events
ADDPREY = pygame.USEREVENT + 1
ADDPLANT = pygame.USEREVENT + 2
ADDBERRY = pygame.USEREVENT + 3
ADDSENSOR = pygame.USEREVENT + 4