import pygame
import os
import sys
from assets.objects.Player import Player
from assets.objects.environnement.Wall import Wall

#sys.path.append(os.path.abspath("/assets/objects/Player.py"))

pygame.init()

#screen_width, screen_height = 1000,1000

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((300, 300))

pygame.display.set_caption("Rogue Like")

running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
 
 
def update_fps():

	fps = str(int(clock.get_fps()))

	fps_text = font.render(fps, 1, pygame.Color("green"))
	return fps_text


wall = Wall(screen, "wall.jpg", 300,300)
wall1 = Wall(screen, "wall.jpg", 450,300)

player = Player(screen, "Isaac.png", 1000,100,[wall, wall1])

img = pygame.image.load(os.path.join("assets/sprites/props", "Isaac's_Room_1.png")).convert_alpha()
image = pygame.transform.scale(img, (1920,1080))

while running:
  screen.fill((0,0,0))

  screen.blit(image,(0,0))

  player.update()
  wall.Draw()
  wall1.Draw()
  screen.blit(update_fps(), (10,0))
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
      running = False 
  clock.tick(60)
  
  pygame.display.update()

pygame.joystick.quit()
pygame.quit()