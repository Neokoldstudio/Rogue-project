import math
import numpy
import pygame
import os
from scripts import MovementRelatives as physics


pygame.init()
pygame.joystick.init()

class Player():
    def __init__(self,screen, sprite, position, props):

        self.joysticks=[pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        for i in self.joysticks:
            i.init()

        pygame.sprite.Sprite.__init__(self)
        self.sqrt2 = math.sqrt(2)

        #sprite and pos on the screen
        self.screen = screen
        self.img = pygame.image.load(os.path.join("assets/sprites/Main_character", sprite)).convert_alpha()
        self.image = pygame.transform.scale(self.img, (450,450))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        #collisions relatives variables
        self.collisionType = "Circle"
        self.colliderXOffset = 225
        self.colliderYOffset = 255
        self.collideRadius = 20
        self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

        #movement variables
        self.speed = 13
        self.props = props
        self.hsp = 0
        self.vsp = 0
       
    def update(self):
        
        key = pygame.key.get_pressed()
        old_x, old_y = self.rect.x, self.rect.y

        #Manette détectée : mouvements gérés par cette dernière
        if (self.joysticks != []):

            JoyMoving = (abs(self.joysticks[0].get_axis(1)) > 0.2) or (abs(self.joysticks[0].get_axis(0)) > 0.2)

            if(JoyMoving):#la valeur retournée par les sticks est superieure à 0.2
                VerDir = self.joysticks[0].get_axis(1)#-
                HorDir = self.joysticks[0].get_axis(0)# | - la direction est égale à la valeur retournée par les sticks
 
            else:#sinon : les directions sont égales à 0
                VerDir = 0
                HorDir = 0

        #sinon : mouvements gérés par le clavier
        else:
            
            KeyLeft = key[pygame.K_q]
            KeyRight = key[pygame.K_d]
            KeyUp = key[pygame.K_z]
            KeyDown = key[pygame.K_s]

            #calcul de la direction horizontale et verticale
            HorDir = KeyRight - KeyLeft
            VerDir = KeyDown - KeyUp
            #correction de la vitesse plus élevée en diagonale
            if(HorDir*VerDir != 0):
                HorDir = HorDir / self.sqrt2
                VerDir = VerDir / self.sqrt2

        #une fonction lerp gère l'accélération et la décélération du personnage
        self.hsp = physics.Lerp(self.hsp, HorDir * self.speed)
        self.vsp = physics.Lerp(self.vsp, VerDir * self.speed)

        #on change la position du joueur en y ajoutant les varibles hsp et vsp
        self.rect.x += round(self.hsp)
        self.rect.y += round(self.vsp)
        self.collisionCenter = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)#on change aussi la position du collider

        #collisions :

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

            elif(i.collisionType == "Circle"):#l'objet avec le lequel on vérifie la collision à une hitbox ronde
                if(physics.DistCircleToCircle(self.collisionCenter, i.collisionCenter, self.collideRadius, i.collideRadius) <= 0):
                    #ici : écrire le code gérant les réactions du joueur à une collisions avec une entitée n'étant pas un mur ( ex : prendre des dégats, etc ... ) 
                    pass

        self.screen.blit(self.image,self.rect)

        #collision debug : 
        #pygame.draw.circle(self.screen, (255,0,0), self.collisionCenter, self.collideRadius)