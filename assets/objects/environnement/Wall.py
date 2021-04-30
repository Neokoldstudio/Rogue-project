import math
import pygame
import os

pygame.init()

class Wall():

    def __init__(self, screen, sprite, position, size):

        self.screen = screen
        self.img = pygame.image.load(os.path.join("assets/sprites/props", sprite)).convert_alpha()
        self.collisionSize = size
        self.image = pygame.transform.scale(self.img, (self.collisionSize[0],self.collisionSize[1]))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        
        #parametres de collision : INDISPENSABLES
        self.collisionCenter = (self.rect.x + self.collisionSize[0]/2, self.rect.y+ self.collisionSize[1]/2) 
        self.collisionType = "Box"

    def Draw(self):

        self.screen.blit(self.image,self.rect)

        #collision debug
        #pygame.draw.rect(self.screen, (255,0,0), (self.rect.x,self.rect.y, self.collisionCenter[0],self.collisionCenter[1])) <--- doesn't work