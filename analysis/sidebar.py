import pygame
from var import *

# draw text on lower sidebar
def write_sidebar_lower(screen, prey_list, start_index):
    y = (SCREEN_HEIGHT*0.4)-(BUFFER*1.5)+(BUFFER*2) + 10
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

# draw a stats distribution bar chart
def create_bar_chart(screen, dist, surface_sidebar_upper_x, surface_sidebar_upper_y):

    ## test draw 1 bar
    # # varaibles
    # x = SURFACE_MAIN_WIDTH + (BUFFER*2) + 10
    # y = BUFFER + 10
    # width = 10
    # height = 20
    # color = pygame.Color("orange")
    # # create surface and rectangle
    # surf = pygame.Surface((width,height))
    # surf.fill(color)
    # rect = surf.get_rect(center=((x+(0.5*width)),(y+(0.5*height))))
    # # draw on screen
    # screen.blit(surf, rect)

    ## draw from array
    # start_x = surface_sidebar_upper_x
    # start_y = surface_sidebar_upper_y
    # n = len(arr)
    # for i in range(n):
    #     draw_bar(screen, arr, i, start_x, start_y)

    ## draw from dist dictionary
    min_bar_height = 0
    max_bar_height = 20
    start_x = surface_sidebar_upper_x
    start_y = surface_sidebar_upper_y
    # index each bar
    index = 0
    n_bars = len(dist)
    # key is trait, value is frequency (count)
    for key, value in dist.items():
        normalized_value = (value - min(dist.values())) / (max(dist.values()) - min(dist.values())) * (max_bar_height - min_bar_height) + min_bar_height
        print(value, min(dist.values()), max(dist.values()), min_bar_height, max_bar_height)
        print(normalized_value)
        if normalized_value == 0 and value > 0:
            normalized_value = 1
        draw_bar(screen, value, normalized_value, max_bar_height, index, n_bars, start_x, start_y)
        index += 1

# draw a single bar
def draw_bar(screen, value, height, max_bar_height, index, n_bars, start_x, start_y):
    spacing = 5
    width = SURFACE_SIDEBAR_WIDTH - (spacing*2)
    
    bar_width = width // n_bars
    bar_height = height

    print(bar_height)

    x = start_x + spacing + (bar_width * index)
    y = start_y + spacing + max_bar_height - bar_height
    # print(start_y,height)
    # print(bar_height+y)
    # create surface and rectangle
    color = pygame.Color("orange")
    surf = pygame.Surface((bar_width,bar_height))
    surf.fill(color)
    rect = surf.get_rect(x=x, y=y)
    # draw on screen
    screen.blit(surf, rect)

# handle scrolling on lower sidebar
def scroll(delta, prey_list, start_index):
    start_index += delta
    max_line_count = round((((SCREEN_HEIGHT*0.6)-(BUFFER*1.5)) // SIDEBAR_LINE_HEIGHT))
    # cant scroll past zero
    if start_index < 0:
        start_index = 0
    # cant scroll past the end
    elif start_index > len(prey_list) - max_line_count:
        start_index = len(prey_list) - max_line_count
    return start_index