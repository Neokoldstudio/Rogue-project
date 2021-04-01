import math
import numpy
import pygame
import os


pygame.init()
pygame.joystick.init()

class Player():
    def __init__(self,screen, sprite, x, y, props):

        self.joysticks=[pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        for i in self.joysticks:
            i.init()

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        
        self.img = pygame.image.load(os.path.join("assets/sprites/Main_character", sprite)).convert_alpha()
        self.image = pygame.transform.scale(self.img, (110,150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.props = props
        self.colliderXOffset = 55
        self.colliderYOffset = 120
        self.collideRadius = 30
        self.colliderPos = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)
        self.hsp = 0
        self.vsp = 0

    def update(self):
        
        #all "physics" functions
        def Lerp(spd, wantedSpeed):
            return (spd*0.8 + wantedSpeed*0.2)

        def lenght(v):
            return (math.sqrt(v[0]*v[0] + v[1]*v[1]))

        def DistCircleToCircle(p1, p2, radius1, radius2):
            distTpl = (p2[0]-p1[0], p2[1]-p1[1])
            return(lenght(distTpl)-(radius1+radius2))
        
        def DistBoxToCircle(p, center, size, radius):
            dx = max(abs(p[0] - center[0]) - size / 2, 0)
            dy = max(abs(p[1] - center[1]) - size / 2, 0)

            distPoint = (dx,dy)
            return lenght(distPoint) - radius

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
            
            KeyLeft = key[pygame.K_a]
            KeyRight = key[pygame.K_d]
            KeyUp = key[pygame.K_w]
            KeyDown = key[pygame.K_s]

            #calcul de la direction horizontale et verticale
            HorDir = KeyRight - KeyLeft
            VerDir = KeyDown - KeyUp
            #correction de la vitesse plus élevée en diagonale
            if(HorDir*VerDir != 0):
                HorDir = HorDir / math.sqrt(2)
                VerDir = VerDir / math.sqrt(2)

        #une fonction lerp gère l'accélération et la décélération du personnage
        self.hsp = Lerp(self.hsp, HorDir * self.speed)
        self.vsp = Lerp(self.vsp, VerDir * self.speed)

        print(self.hsp, self.vsp)
        
        #on change la position du joueur en y ajoutant les varibles hsp et vsp
        self.rect.x += self.hsp
        self.rect.y += self.vsp
        self.colliderPos = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)#on change aussi la position du collider

        #collisions :
        for i in self.props:
            if(i.collisionType == "Box"):#l'objet avec le lequel on vérifie la collision à une hitbox carrée
                if(DistBoxToCircle(self.colliderPos, i.collisionCenter,i.collisionSize, self.collideRadius)<= 0):
                    self.rect.x = old_x
                    self.rect.y = old_y
                    self.colliderPos = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

            elif(i.collisionType == "Circle"):#l'objet avec le lequel on vérifie la collision à une hitbox ronde
                if(DistCircleToCircle(self.colliderPos, i.collisionCenter, self.collideRadius, i.collideRadius) <= 0):
                    self.rect.x = old_x
                    self.rect.y = old_y
                    self.colliderPos = (self.rect.x + self.colliderXOffset, self.rect.y + self.colliderYOffset)

        self.screen.blit(self.image,self.rect)
        pygame.draw.circle(self.screen, (255,0,0), self.colliderPos, self.collideRadius)