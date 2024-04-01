import pygame
from var import *

# draw text on sidebar
def write_sidebar(screen, prey_list, start_index):
    y = BUFFER + 10
    if start_index < 0:
        start_index = 0
    for i, spr in enumerate(prey_list[start_index:]):
        text_main = "Prey ["+str(start_index+i)+"]:    "
        text_dtl = str(spr.size) + "    " + str(spr.speed) + "    " + str(spr.sense)
        text_main_surface = pygame.font.Font(None, SIDEBAR_FONT_SIZE).render(text_main, True, COLOR_SIDEBAR_TEXT_MAIN)
        text_dtl_surface = pygame.font.Font(None, SIDEBAR_FONT_SIZE).render(text_dtl, True, COLOR_SIDEBAR_TEXT_DETAIL)
        screen.blit(text_main_surface, (SCREEN_WIDTH - SURFACE_SIDEBAR_WIDTH - BUFFER + 10, y))
        screen.blit(text_dtl_surface, (SCREEN_WIDTH - SURFACE_SIDEBAR_WIDTH - BUFFER + 10 + text_main_surface.get_width(), y))
        y += SIDEBAR_LINE_HEIGHT
        if y > SCREEN_HEIGHT-BUFFER:
            break

# Function to handle scrolling
def scroll(delta, prey_list, start_index):
    start_index += delta
    if start_index < 0:
        start_index = 0
    elif start_index > len(prey_list) - ((SCREEN_HEIGHT-(BUFFER*2)) // SIDEBAR_LINE_HEIGHT):
        start_index = len(prey_list) - ((SCREEN_HEIGHT-(BUFFER*2)) // SIDEBAR_LINE_HEIGHT)
    return start_index