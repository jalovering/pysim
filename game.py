import pygame
from pygame.locals import *
from biota.Player import Player
from biota.Plant import Plant
from biota.Prey import Prey
from biota.Sensor import Sensor
from biota.Berry import Berry
from var import *
import random
import analysis.sidebar as sidebar
import analysis.analyze as analyze
from analysis.Bar import Bar

# initialize pygame
pygame.init()
isInitialFrame = True

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
surface = pygame.Surface((SURFACE_MAIN_WIDTH, SCREEN_HEIGHT-(BUFFER*2)))
surface_sidebar_upper = pygame.Surface((SURFACE_SIDEBAR_WIDTH, (SCREEN_HEIGHT*0.4)-(BUFFER*1.5)))
surface_sidebar_lower = pygame.Surface((SURFACE_SIDEBAR_WIDTH, (SCREEN_HEIGHT*0.6)-(BUFFER*1.5)))
pygame.display.set_caption('pysim') 

surface_sidebar_upper_x = (BUFFER*2)+SURFACE_MAIN_WIDTH
surface_sidebar_upper_y = BUFFER
surface_sidebar_lower_x = (BUFFER*2)+SURFACE_MAIN_WIDTH
surface_sidebar_lower_y = (SCREEN_HEIGHT*0.4)-(BUFFER*1.5)+(BUFFER*2)

# # custom event - add prey
# ADDPREY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDPREY, int(40000/PLAY_SPEED_MOD))

# custom event - add plant
ADDPLANT = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPLANT, int(30000/PLAY_SPEED_MOD))

# sprite groups
prey_group = pygame.sprite.Group()
sensor_group = pygame.sprite.Group()
plant_group = pygame.sprite.Group()
berry_group = pygame.sprite.Group()
bar_group = pygame.sprite.Group()
bar_initial_group = pygame.sprite.Group()
all_group = pygame.sprite.Group()

# player object
player = Player()
all_group.add(player)

# initial prey object
for i in range(6):
    new_prey = Prey(
        color=(1,1,1), 
        size=random.randint(8,12),
        speed=round(random.uniform(0.8, 1.2),1),
        sense=random.randint(80,120))
    # new_prey = Prey(color=(1,1,1))
    prey_group.add(new_prey)
    all_group.add(new_prey)

# for i in range(1):
#     new_prey = Prey(color=(1,1,1),size=15)
#     prey_group.add(new_prey)
#     all_group.add(new_prey)

# initial plant object
for i in range(8):
    new_plant = Plant(
        size=random.randint(8,10)
        )
    plant_group.add(new_plant)
    all_group.add(new_plant)

# index of first displayed prey in list
# this changes as you scroll
start_index = 0

# game loop
clock = pygame.time.Clock()
running = True
while running: 

    ## reset for this frame
    # reset screen and surface
    screen.fill(COLOR_BG) 
    surface.fill(COLOR_SURFACE)
    surface_sidebar_lower.fill(COLOR_SURFACE_SIDEBAR)
    surface_sidebar_upper.fill(COLOR_SURFACE_SIDEBAR)
    screen.blit(surface,(BUFFER,BUFFER))
    screen.blit(surface_sidebar_upper,(surface_sidebar_upper_x, surface_sidebar_upper_y))
    screen.blit(surface_sidebar_lower,(surface_sidebar_lower_x, surface_sidebar_lower_y))
    # delete last frame bars
    for entity in bar_group:
        if isHoverFrame and entity.rect.collidepoint(pygame.mouse.get_pos()):
            for prey in prey_group:
                prey.highlightOff()
        entity.kill()
        del entity
    
    ## event handler
    for event in pygame.event.get(): 
        # QUIT - window close      
        if event.type == pygame.QUIT: 
            running = False
        # lower sidebar scroll
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
        # add bar
        if event.type == ADDBAR:
            new_bar = Bar(
                color=event.color,
                x = event.x,
                y = event.y,
                height = event.height,
                width = event.width,
                groupedValue = event.groupedValue,
                gene = event.gene
            )
            if event.isInitial:
                bar_initial_group.add(new_bar)
            else:
                bar_group.add(new_bar)
            all_group.add(new_bar)

    ## run updates
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

    ## prepare sidebar (technically representing the last frame)
    # prep data
    prey_stats = analyze.create_prey_stats(prey_group.sprites())
    if isInitialFrame:
        prey_stats_initial = prey_stats
        # upper sidebar: datavis - initial
        sidebar.draw_sidebar_upper(screen, surface_sidebar_upper_x, surface_sidebar_upper_y, prey_stats_initial, isInitial=True)
    else:
        # upper sidebar: datavis - current
        sidebar.draw_sidebar_upper(screen, surface_sidebar_upper_x, surface_sidebar_upper_y, prey_stats, isInitial=False)
    # lower sidebar: list
    sidebar.write_sidebar_lower(screen, prey_group.sprites(), start_index)
    
    ## draw current frame
    # draw histograms
    isHoverFrame = False
    # draw bars
    for entity in bar_initial_group:
        screen.blit(entity.surf, entity.rect)
    for entity in bar_group:
        # check for mouse hover
        if entity.rect.collidepoint(pygame.mouse.get_pos()):
            entity.hoverOn(prey_group)
            isHoverFrame = True
        screen.blit(entity.surf, entity.rect)
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

    ### TESTING START
    # print(pygame.time.get_ticks())
    # print(prey_stats[:, 0])
    # print(prey_stats)
    # print(len(prey_group))
    # print(len(sensor_group))
    # print(len(plant_group))
    # print(len(berry_group))
    # print(len(bar_group))
    # print(len(bar_initial_group))
    # print(len(all_group))
    ### TESTING END

    ## update display
    pygame.display.flip()
    clock.tick(FPS*FPS_MOD)
    isInitialFrame = False