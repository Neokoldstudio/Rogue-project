import math
import pygame
import os
from scripts import MovementRelatives as physics
from threading import Timer

pygame.init()

class Enemy():
    def __init__(self,screen, position, target, props, enemyType):

        #sprite and pos on the screen
        self.enemyType = enemyType
        self.selector = {"Zombie" : (1,"IsaacZombie.png", (70,100), (35,70,30), 5, 5), "Fly" : (2,"fly.png",(50,50),(25,25,10),6, 3)}
        self.screen = screen
        self.img = pygame.image.load(os.path.join("assets/sprites/ennemies", self.selector[self.enemyType][1])).convert_alpha()
        self.image = pygame.transform.scale(self.img, self.selector[self.enemyType][2])
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
 
        #collisions relatives variables
        self.props = props
        self.collisionType = "Circle"
        self.EntityType = "Enemy"
        self.colliderXOffset = self.selector[self.enemyType][3][0]
        self.colliderYOffset = self.selector[self.enemyType][3][1]
        self.collideRadius = self.selector[self.enemyType][3][2]
        self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

        #pathfinding varibles
        self.target = target
       
        #ennemy variables
        self.enemyIndex = self.selector[enemyType][0]
        self.speed = self.selector[enemyType][4]
        self.hsp = 0
        self.vsp = 0
        self.hp = self.selector[enemyType][5]
        self.coolDown = 0.5
        self.hit = False

        #debug variables:
        self.debug = False

    def Draw(self):

        def resetHit():
            self.hit = False

        def Zombie():#logique pour l'ennemi "Zombie"
            old_x, old_y = self.rect.x, self.rect.y
            GoToVec = (self.target.collisionCenter[0] - self.collisionCenter[0], self.target.collisionCenter[1] - self.collisionCenter[1])
            distance = physics.lenght(GoToVec)

            GoToVec = ((GoToVec[0]/distance)*self.speed,(GoToVec[1]/distance)*self.speed)

            if(distance > 1):
                
                self.hsp, self.vsp = physics.Lerp(self.hsp, GoToVec[0], 0.8), physics.Lerp(self.vsp, GoToVec[1], 0.8)

                self.rect.x += self.hsp
                self.rect.y += self.vsp

                self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)  
            
            if(physics.DistCircleToCircle(self.collisionCenter, self.target.collisionCenter, self.collideRadius, self.target.collideRadius) <= -1): #collision avec le joueur

                self.hsp, self.vsp = physics.Lerp(self.hsp, GoToVec[0]*(-self.speed), 0.8), physics.Lerp(self.vsp, GoToVec[1]*(-self.speed), 0.8) #/!\ le joueur peut pousser les mobs dans le mur et les bloquer /!\

                self.rect.x += self.hsp
                self.rect.y += self.vsp

                self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

            if(self.target.SwordList != []): #quand l'ennemi se fait fait frapper par le joueur
                if(physics.DistBoxToCircle(self.collisionCenter, self.target.SwordList[0].collisionCenter, self.target.SwordList[0].collisionSize, self.collideRadius) <= 0 and not self.hit):
                    self.hit = True
                    self.hsp, self.vsp = physics.Lerp(self.hsp, GoToVec[0]*(-self.speed*5), 0.8), physics.Lerp(self.vsp, GoToVec[1]*(-self.speed*5), 0.8)

                    self.rect.x += self.hsp
                    self.rect.y += self.vsp

                    self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

                    self.hp -= 1

                    t = Timer(self.coolDown, resetHit)
                    t.start()

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
                #pygame.draw.line(self.screen, (0,255,0), self.collisionCenter, (GoToVec[0] + self.collisionCenter[0], GoToVec[1] + self.collisionCenter[1]), width = 3)
                #pygame.draw.line(self.screen, (255,0,0), self.collisionCenter, self.target.collisionCenter, width = 1)

        def Fly():#logique pour l'ennemi "Fly"
            GoToVec = (self.target.collisionCenter[0] - self.collisionCenter[0], self.target.collisionCenter[1] - self.collisionCenter[1])
            distance = physics.lenght(GoToVec)

            GoToVec = ((GoToVec[0]/distance)*self.speed,(GoToVec[1]/distance)*self.speed)

            if(distance > 1):
                
                self.hsp, self.vsp = physics.Lerp(self.hsp, GoToVec[0], 0.8), physics.Lerp(self.vsp, GoToVec[1], 0.8) # cette partie calcule un vecteur direction de l'ennemi jusqu'au joueur

                self.rect.x += self.hsp
                self.rect.y += self.vsp

                self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)  

            if(physics.DistCircleToCircle(self.collisionCenter, self.target.collisionCenter, self.collideRadius, self.target.collideRadius) <= -1): #collision avec le joueur

                self.hsp, self.vsp = physics.Lerp(self.hsp, GoToVec[0]*(-self.speed), 0.8), physics.Lerp(self.vsp, GoToVec[1]*(-self.speed), 0.8) #/!\ le joueur peut pousser les mobs dans le mur et les bloquer /!\

                self.rect.x += self.hsp
                self.rect.y += self.vsp

                self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

            if(self.target.SwordList != []):
                if(physics.DistBoxToCircle(self.collisionCenter, self.target.SwordList[0].collisionCenter, self.target.SwordList[0].collisionSize, self.collideRadius) <= 0 and not self.hit):
                    self.hit = True
                    self.hsp, self.vsp = physics.Lerp(self.hsp, GoToVec[0]*(-self.speed*5), 0.8), physics.Lerp(self.vsp, GoToVec[1]*(-self.speed*5), 0.8)

                    self.rect.x += self.hsp
                    self.rect.y += self.vsp

                    self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

                    self.hp -= 1

                    t = Timer(self.coolDown, resetHit)
                    t.start()

            self.screen.blit(self.image, self.rect)

            #collision and targetting debug : 
            if(self.debug):
                pygame.draw.circle(self.screen, (255,0,0), self.collisionCenter, self.collideRadius)
                #pygame.draw.line(self.screen, (0,255,0), self.collisionCenter, (GoToVec[0] + self.collisionCenter[0], GoToVec[1] + self.collisionCenter[1]), width = 3)
                #pygame.draw.line(self.screen, (255,0,0), self.collisionCenter, self.target.collisionCenter, width = 1)


        def switchState(enemyType): # state machine permettant de changer le type d'ennemi
            switcher = {
                1: Zombie,
                2: Fly,
            }
            
            func = switcher.get(enemyType)
            func()
        
        switchState(self.enemyIndex)