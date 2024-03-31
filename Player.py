import pygame
from Creature import Creature
from var import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

class Player(Creature):
    def __init__(self, color=COLOR_PLAYER, size=20, speed=2, status="moving", statusLastUpdated=0, hunger=0, age=0):
        super(Player, self).__init__(color, size, speed, status, statusLastUpdated, hunger, age)
        self.surf = pygame.Surface((self.size, self.size*1.5))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys):
        # move player
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -1*self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 1*self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1*self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(1*self.speed, 0)
        # keep in bounds
        if self.rect.left < BUFFER:
            self.rect.left = BUFFER
        if self.rect.right > SURFACE_MAIN_WIDTH+BUFFER:
            self.rect.right = SURFACE_MAIN_WIDTH+BUFFER
        if self.rect.top <= BUFFER - self.size:
            self.rect.top = BUFFER - self.size
        if self.rect.bottom >= SCREEN_HEIGHT-BUFFER:
            self.rect.bottom = SCREEN_HEIGHT-BUFFER