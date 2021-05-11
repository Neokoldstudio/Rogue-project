import math
import pygame
import os

class Sword():
    def __init__(self,screen,position, size):
        self.screen = screen
        self.collisionSize = size
        self.rect = pygame.Rect(position[0],position[1],position[0]+self.collisionSize[0], position[1]+self.collisionSize[1])
        self.rect.x = position[0]
        self.rect.y = position[1]
        
        #parametres de collision : INDISPENSABLES
        self.collisionCenter = (self.rect.x + self.collisionSize[0]/2, self.rect.y+ self.collisionSize[1]/2)

    def Draw(self):
        pygame.draw.circle(self.screen, (255,0,0), self.collisionCenter, self.collisionSize[0])
        pass