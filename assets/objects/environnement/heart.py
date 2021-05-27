import pygame
import os

class Heart():
    def __init__(self, screen, position, player):

        self.screen = screen
        self.img = pygame.image.load(os.path.join("assets/sprites/health" , "heart.png")).convert_alpha()
        self.image = pygame.transform.scale(self.img, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.player = player

        #collisions variables
        self.collisionType = "Circle"
        self.EntityType = "heart"
        self.colliderXOffset = 24
        self.colliderYOffset = 23
        self.collideRadius = 20
        self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

        self.used = False

    def Draw(self):

        #pygame.draw.circle(self.screen, (0,255,0), self.collisionCenter, self.collideRadius) #debug 
        self.screen.blit(self.image,self.rect)
        