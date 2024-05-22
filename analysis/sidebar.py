import pygame
import analysis.analyze as analyze
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

# draw histograms
def draw_sidebar_upper(screen, surface_sidebar_upper_x, surface_sidebar_upper_y, prey_stats):
    title_height = 30
    histogram_height = 50
    x = surface_sidebar_upper_x
    y = surface_sidebar_upper_y
    index = 0 # prey_stats 2d array index
    genes = ["size", "speed", "sense"]
    # create all 3 histograms
    for gene in genes:
        if gene == "size":
            gene_min, gene_max, gene_decimals = SIZE_MIN, SIZE_MAX, SIZE_DECIMALS
        elif gene == "speed":
            gene_min, gene_max, gene_decimals = SPEED_MIN, SPEED_MAX, SPEED_DECIMALS
        elif gene == "sense":
            gene_min, gene_max, gene_decimals = SENSE_MIN, SENSE_MAX, SENSE_DECIMALS
        dist = analyze.create_frequency_dist(prey_stats[:, index], gene, gene_min, gene_max, gene_decimals)
        draw_title(screen, gene, x, y)
        y += title_height
        draw_histogram(screen, gene, dist, x, y)
        y += histogram_height
        index += 1
        
# draw histogram title
def draw_title(screen, gene, x, y):
    text = gene.upper()
    text_surface = pygame.font.Font(None, SIDEBAR_FONT_SIZE).render(text, True, COLOR_SIDEBAR_TEXT_MAIN)
    screen.blit(text_surface, (x+10, y+10))

# draw a stats distribution bar chart
def draw_histogram(screen, gene, dist, x, y):
    ## draw from frequency dictionary
    min_bar_height = 0
    max_bar_height = 20
    start_x = x
    start_y = y
    # index each bar
    index = 0
    n_bars = len(dist)
    # key is trait, value is frequency (count)
    for groupedValue, value in dist.items():
        minVal = min(dist.values())
        maxVal = max(dist.values())
        if minVal + maxVal == 0:
            break
        value = float(value)
        # normalize gene value for bar height
        normalized_value = round((value - minVal) / (maxVal - minVal) * (max_bar_height - min_bar_height) + min_bar_height)
        # force smallest values to 1px if they would have been rounded to zero
        if normalized_value == 0 and value > 0:
            normalized_value = 1
        if value != 0:
            draw_bar(screen, normalized_value, max_bar_height, index, n_bars, start_x, start_y, groupedValue, gene)
        index += 1

# draw a single bar
def draw_bar(screen, height, max_bar_height, index, n_bars, start_x, start_y, groupedValue, gene):
    # define size and positioning
    buffer = 10
    spacing = 2
    width = SURFACE_SIDEBAR_WIDTH - (buffer*2)
    bar_width = (width-(spacing*(n_bars-1))) // n_bars
    bar_height = height
    if index == 0:
        bar_x = start_x + buffer + bar_width*index
    else:
        bar_x = start_x + buffer + bar_width*index + spacing*index
    bar_y = start_y + spacing + max_bar_height - bar_height
    # create surface and rectangle
        # color = COLOR_SIDEBAR_TEXT_DETAIL
        # surf = pygame.Surface((bar_width,bar_height))
        # surf.fill(color)
        # rect = surf.get_rect(x=bar_x, y=bar_y)
        # draw on screen
        # screen.blit(surf, rect)
    # create bar
    add_bar_event = pygame.event.Event(
        ADDBAR,
        color=COLOR_SIDEBAR_TEXT_DETAIL,
        x = bar_x,
        y = bar_y,
        height = bar_height,
        width = bar_width,
        groupedValue = groupedValue,
        gene = gene
    )
    pygame.event.post(add_bar_event)    

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