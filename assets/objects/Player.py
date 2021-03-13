import pygame
import os


pygame.init()

class Player():
    def __init__(self,screen, sprite, x, y):

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        
        self.img = pygame.image.load(os.path.join("assets/sprites/Main_character", sprite)).convert_alpha()
        self.image = pygame.transform.scale(self.img, (250,250))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):

        key = pygame.key.get_pressed()

        
        speed = 9

        KeyLeft = key[pygame.K_q]
        KeyRight = key[pygame.K_d]
        KeyUp = key[pygame.K_z]
        KeyDown = key[pygame.K_s]

        HorDir = KeyRight - KeyLeft
        VerDir = KeyDown - KeyUp

        self.rect.x += speed * HorDir
        self.rect.y += speed * VerDir

        self.screen.blit(self.image,self.rect)