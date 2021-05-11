import math
import numpy
import pygame
import os
from scripts import MovementRelatives as physics
from assets.objects.PlayerSword import Sword
from threading import Timer


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

        #player variables
        self.hp = 6
        self.kill = True
        self.hit = False
        self.speed = 13
        self.props = props
        self.hsp = 0
        self.vsp = 0
        self.invincibilityCooldown = 1.0
        self.SwordList = []

    def Draw(self): pass
       
    def update(self):

        HitPos = {(0,1):Sword(self.screen, (self.collisionCenter[0] + 40, self.collisionCenter[1]-40), (80,80)), #dictionnaire faisant correspondre les inputs  
                       (0,-1):Sword(self.screen, (self.collisionCenter[0] - 100, self.collisionCenter[1] - 30), (80,80)),
                       (-1,0):Sword(self.screen, (self.collisionCenter[0] - 35, self.collisionCenter[1]-100), (80,80)),
                       (1,0):Sword(self.screen, (self.collisionCenter[0] - 30, self.collisionCenter[1] + 40), (80,80))}

        def invicEnd(): #les quatres fonctions qui suivent gèrent des cooldown, FlashEnd permet de faire passer le personnage en blanc
            self.hit = False
        def FlashEnd():
            x,y = self.rect.x, self.rect.y

            self.img = pygame.image.load(os.path.join("assets/sprites/Main_character", "test_idle.png")).convert_alpha()
            self.image = pygame.transform.scale(self.img, (450,450))
            self.rect = self.image.get_rect()

            self.rect.x = x
            self.rect.y = y
        def HitCool():
            self.kill = True
        def HitDelete():
            self.SwordList.pop()

        key = pygame.key.get_pressed()
        old_x, old_y = self.rect.x, self.rect.y

        #Manette détectée : mouvements gérés par cette dernière
        if (self.joysticks != []):

            JoyMoving_left = (abs(self.joysticks[0].get_axis(1)) > 0.2) or (abs(self.joysticks[0].get_axis(0)) > 0.2)
            JoyMoving_right = (abs(self.joysticks[0].get_axis(3)) > 0.2) or (abs(self.joysticks[0].get_axis(2)) > 0.2)

            if(JoyMoving_left):#la valeur retournée par les sticks est superieure à 0.2
                VerDir = self.joysticks[0].get_axis(1)#-
                HorDir = self.joysticks[0].get_axis(0)# | - la direction est égale à la valeur retournée par les sticks
 
            else:#sinon : les directions sont égales à 0
                VerDir = 0
                HorDir = 0

            if(JoyMoving_right and self.kill):
                self.kill = False
                if(abs(self.joysticks[0].get_axis(3)) > abs(self.joysticks[0].get_axis(2))) : HitList = (numpy.sign(self.joysticks[0].get_axis(3)), 0)
                else:HitList = (0, numpy.sign(self.joysticks[0].get_axis(2)))

                self.SwordList.append(HitPos[HitList])

                self.SwordList[0].Draw()

                t = Timer(self.invincibilityCooldown/3, HitCool)
                t2 = Timer(self.invincibilityCooldown/10, HitDelete)
                t.start()
                t2.start()

        #sinon : mouvements gérés par le clavier
        else:
            #détection des touches pour le déplacement
            KeyLeft = key[pygame.K_q]
            KeyRight = key[pygame.K_d]
            KeyUp = key[pygame.K_z]
            KeyDown = key[pygame.K_s]

            #détection des touches pour frapper
            HitLeft = key[pygame.K_LEFT]
            HitRight = key[pygame.K_RIGHT]
            HitUp = key[pygame.K_UP]
            HitDown = key[pygame.K_DOWN]

            #calcul de la direction horizontale et verticale
            HorDir = KeyRight - KeyLeft
            VerDir = KeyDown - KeyUp
            #correction de la vitesse plus élevée en diagonale
            if(HorDir*VerDir != 0):
                HorDir = HorDir / self.sqrt2
                VerDir = VerDir / self.sqrt2

            HorHit = HitRight - HitLeft
            VerHit = HitDown - HitUp

            if(self.kill and (HorHit, VerHit)!=(0,0)):
                self.kill = False

                if((HorHit,VerHit) in HitPos):
                    HitList = (VerHit,HorHit)

                self.SwordList.append(HitPos[HitList])

                self.SwordList[0].Draw()

                t = Timer(self.invincibilityCooldown/3, HitCool)
                t2 = Timer(self.invincibilityCooldown/10, HitDelete)
                t.start()
                t2.start()

        #une fonction lerp gère l'accélération et la décélération du personnage
        self.hsp = physics.Lerp(self.hsp, HorDir * self.speed,0.87)
        self.vsp = physics.Lerp(self.vsp, VerDir * self.speed,0.87)

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

            elif(i.collisionType == "Circle" and i != self):#l'objet avec le lequel on vérifie la collision à une hitbox ronde
                if(physics.DistCircleToCircle(self.collisionCenter, i.collisionCenter, self.collideRadius, i.collideRadius) <= 0):

                    if(i.EntityType == "Enemy" and not self.hit):
                        self.hit = True
                        self.hp -= 1

                        if(self.hp <= 0):
                            self.hp = 0
                            #logique de la mort du perso

                        x,y = self.rect.x, self.rect.y

                        self.img = pygame.image.load(os.path.join("assets/sprites/Main_character", "test_idle_flash.png")).convert_alpha()
                        self.image = pygame.transform.scale(self.img, (450,450))
                        self.rect = self.image.get_rect()

                        self.rect.x = x
                        self.rect.y = y

                        t = Timer(self.invincibilityCooldown, invicEnd)
                        flash = Timer(self.invincibilityCooldown/7, FlashEnd)
                        t.start()
                        flash.start()

                        print(self.hp)

        self.screen.blit(self.image,self.rect)

        #collision debug : 
        pygame.draw.circle(self.screen, (255,0,0), self.collisionCenter, self.collideRadius)