import pygame
### CONSTANTS ###
## color
# Tol Colorblind Palette
# c1 = (51,34,136) #332288
# c2 = (17,119,51) #117733
# c3 = (68,170,153) #44AA99
# c4 = (136,204,238) #88CCEE
# c5 = (221,204,119) #DDCC77
# c6 = (204,102,119) #CC6677
# c7 = (170,68,153) #AA4499
# c8 = (136,34,85) #882255
COLOR_BG = (118,133,136)
COLOR_SURFACE = (147,168,171)
COLOR_SURFACE_SIDEBAR = (85, 93, 94)
COLOR_SIDEBAR_TEXT_MAIN = (225, 225, 225)
COLOR_SIDEBAR_TEXT_DETAIL = (31, 173, 117)
COLOR_PREY = (106,116,158)
COLOR_PLANT = (112, 156, 124)
COLOR_BERRY = (194, 114, 118)
COLOR_PLAYER = (158, 116, 106)
COLOR_SENSOR = (175, 175, 175, 100)
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
SURFACE_MAIN_WIDTH = 1000
SURFACE_SIDEBAR_WIDTH = 190
BUFFER = 30
## regular attributes
PREY_DEFAULT_SIZE = 10
PREY_DEFAULT_SPEED = 1.0
PLANT_SIZE_MAX = 10
PLANT_BERRIES_MAX = 10
## time-based attributes
PREY_EAT_TIME = 1000 # takes 1000ms to eat
PREY_HUNGER_INTERVAL = 10000 # gain 1 hunger every 10s
PREY_DYING_TIME = 3000 # takes 3000ms to die
PREY_MATE_INTERVAL = 60000 # mating eligibility every 60s
PLANT_GROWTH_INTERVAL = 10000 # grow every 10s
## sidebar
SIDEBAR_FONT_SIZE = 16
SIDEBAR_LINE_HEIGHT = SIDEBAR_FONT_SIZE + 5
SIDEBAR_SCROLL_SPEED = 1
## custom events
ADDPREY = pygame.USEREVENT + 1
ADDPLANT = pygame.USEREVENT + 2
ADDBERRY = pygame.USEREVENT + 3
ADDSENSOR = pygame.USEREVENT + 4
ADDPREYBABY = pygame.USEREVENT + 5
## PLAY SPEED
FPS = 60
PLAY_SPEED_MOD = 12
FPS_MOD = 1