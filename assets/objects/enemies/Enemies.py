import pygame
import os

pygame.init()

class Enemy():
    def __init__(self,screen, sprite, position):

        #sprite and pos on the screen
        self.screen = screen
        self.img = pygame.image.load(os.path.join("assets/sprites/ennemies", sprite)).convert_alpha()
        self.image = pygame.transform.scale(self.img, (450,450))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
 
        #collisions relatives variables
        self.collisionType = "Circle"
        self.colliderXOffset = 225
        self.colliderYOffset = 255
        self.collideRadius = 20
        self.colliderPos = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)
       
        #movement variables
        self.speed = 10
        self.props = props
        self.hsp = 0
        self.vsp = 0
        

    def Draw(self):

        #pygame.screen.blit(self.image, self.rect)

        #collision debug : 
        pygame.draw.circle(self.screen, (255,0,0), self.colliderPos, self.collideRadius)
