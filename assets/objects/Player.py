import math
import pygame
import os


pygame.init()
pygame.joystick.init()

class Player():
    def __init__(self,screen, sprite, x, y):

        self.joysticks=[pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        for i in self.joysticks:
            i.init()

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        
        self.img = pygame.image.load(os.path.join("assets/sprites/Main_character", sprite)).convert_alpha()
        self.image = pygame.transform.scale(self.img, (250,250))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):

        def Lerp(A,B,C):
            value = (C*A) + ((1-C)*B)
            return value

        key = pygame.key.get_pressed()

        if (self.joysticks != []):

            speed = 5

            VerDir = self.joysticks[0].get_axis(1)
            HorDir = self.joysticks[0].get_axis(0)

        else:
            
            speed = 4

            KeyLeft = key[pygame.K_q]
            KeyRight = key[pygame.K_d]
            KeyUp = key[pygame.K_z]
            KeyDown = key[pygame.K_s]

            HorDir = KeyRight - KeyLeft
            VerDir = KeyDown - KeyUp

            if(HorDir*VerDir != 0):
                HorDir = 0.6 * HorDir
                VerDir = 0.6 * VerDir

        if (math.sqrt(VerDir**2) > 0.2 or math.sqrt(HorDir**2) > 0.2):

                self.rect.x += speed * HorDir
                self.rect.y += speed * VerDir

                
        self.screen.blit(self.image,self.rect)