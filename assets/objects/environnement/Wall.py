import math
import pygame
import os

pygame.init()

class Wall():

    def __init__(self, screen, sprite, x, y):

        self.screen = screen
        self.img = pygame.image.load(os.path.join("assets/sprites/props", sprite)).convert_alpha()
        self.image = pygame.transform.scale(self.img, (150,150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def Draw(self):

        self.screen.blit(self.image,self.rect)