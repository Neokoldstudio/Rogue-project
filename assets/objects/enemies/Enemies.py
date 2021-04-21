import math
import pygame
import os
from scripts import MovementRelatives as physics

pygame.init()

class Enemy():
    def __init__(self,screen, sprite, position, target, props):

        #sprite and pos on the screen
        self.screen = screen
        self.img = pygame.image.load(os.path.join("assets/sprites/ennemies", sprite)).convert_alpha()
        self.image = pygame.transform.scale(self.img, (70,100))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
 
        #collisions relatives variables
        self.props = props
        self.collisionType = "Circle"
        self.EntityType = "Ennemy"
        self.colliderXOffset = 35
        self.colliderYOffset = 70
        self.collideRadius = 30
        self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

        #pathfinding varibles
        self.target = target
       
        #movement variables
        self.speed = 5
        self.hsp = 0
        self.vsp = 0

        #debug variables:
        self.debug = False
        

    def Draw(self):

        old_x, old_y = self.rect.x, self.rect.y
        GoToVec = (self.target.collisionCenter[0] - self.collisionCenter[0], self.target.collisionCenter[1] - self.collisionCenter[1])
        distance = physics.lenght(GoToVec)

        if(distance > 2):
            
            GoToVec = ((GoToVec[0]/distance)*self.speed,(GoToVec[1]/distance)*self.speed)

            self.rect.x += GoToVec[0]
            self.rect.y += GoToVec[1]

            self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

        for i in self.props:
            if(i.collisionType == "Box"):#l'objet avec le lequel on vérifie la collision à une hitbox carrée
                if(physics.DistBoxToCircle(self.collisionCenter, i.collisionCenter,i.collisionSize, self.collideRadius)<= 0):

                    IsXin = (self.collisionCenter[0] > i.rect.x) and (self.collisionCenter[0] < (i.rect.x + i.collisionSize[0]))
                    IsYin = (self.collisionCenter[1] > i.rect.y) and (self.collisionCenter[1] < (i.rect.y + i.collisionSize[1]))

                    if( not IsXin and IsYin):
                        self.rect.x = old_x
                    elif(IsXin and not IsYin):
                        self.rect.y = old_y
                    else:
                        self.rect.x = old_x
                        self.rect.y = old_y
                    self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)
            

        self.screen.blit(self.image, self.rect)

        #collision and targetting debug : 
        if(self.debug):
            pygame.draw.circle(self.screen, (255,0,0), self.collisionCenter, self.collideRadius)
            pygame.draw.line(self.screen, (0,255,0), self.collisionCenter, (GoToVec[0] + self.collisionCenter[0], GoToVec[1] + self.collisionCenter[1]), width = 3)
            pygame.draw.line(self.screen, (255,0,0), self.collisionCenter, self.target.collisionCenter, width = 1)
