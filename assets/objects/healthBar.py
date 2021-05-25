import pygame
import os

class Health():
    def __init__(self, screen, position, Player):
        self.screen = screen
        self.position = position
        self.player = Player

        self.sprites = [("assets/sprites/health","heart6.png"),
                        ("assets/sprites/health","heart5.png"),
                        ("assets/sprites/health","heart4.png"),
                        ("assets/sprites/health","heart3.png"),
                        ("assets/sprites/health","heart2.png"),
                        ("assets/sprites/health","heart1.png"),
                        ("assets/sprites/health","heart0.png")]
                        

    def Update(self):
        self.img = pygame.image.load(os.path.join(self.sprites[self.player.hp][0], self.sprites[self.player.hp][1])).convert_alpha()
        self.image = pygame.transform.scale(self.img, (128,128))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.screen.blit(self.image,self.rect)