import math
import pygame
import os

pygame.init()

class InvisibleWall():

    def __init__(self, screen, x, y, size):

        self.screen = screen
        self.collisionSize = size
        self.rect = pygame.Rect(x,y,x+self.collisionSize[0], y+self.collisionSize[1])
        self.rect.x = x
        self.rect.y = y
        
        #parametres de collision : INDISPENSABLES
        self.collisionCenter = (self.rect.x + self.collisionSize[0]/2, self.rect.y+ self.collisionSize[1]/2) 
        self.collisionType = "Box"

    def Draw(self):
        #pygame.draw.rect(self.screen, (0,0,255, 10), (self.rect.x,self.rect.y, self.rect.x + self.collisionSize[0],self.rect.y + self.collisionSize[1]))
        pass
        