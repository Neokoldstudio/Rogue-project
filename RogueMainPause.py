import pygame
import os
import sys
from assets.objects.Player import Player
from assets.objects.enemies.Enemies import Enemy
from assets.objects.environnement.Wall import Wall
from assets.objects.environnement.InvisibleWall import InvisibleWall

def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def sub(u, v):
    return [u[i]-v[i] for i in range(len(u))]

def normalize(v):
    return [v[i]/magnitude(v)  for i in range(len(v))]

#sys.path.append(os.path.abspath("/assets/objects/Player.py"))

pygame.init()

#screen_width, screen_height = 1000,1000

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((600, 600))

pygame.display.set_caption("Rogue Like")

running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
 
 
def update_fps():

	fps = str(int(clock.get_fps()))

	fps_text = font.render(fps, 1, pygame.Color("green"))
	return fps_text


#création de toutes les instances des objets 
IWallTop = InvisibleWall(screen, (0, 180), (1920,2))
IWallLeft = InvisibleWall(screen, (200, 0), (2,1080))
IWallRight = InvisibleWall(screen, (1718, 0), (2,1080))
IWallDown = InvisibleWall(screen, (0, 888), (1920,2))
wall = Wall(screen, "wall.jpg", (600,150),(150,150))

props = [IWallTop, IWallLeft, IWallRight, IWallDown, wall]

player = Player(screen, "test_idle.png", (1000,100),props)

Enemy1 = Enemy(screen, (300,200),player, props,"Fly")
Enemy2 = Enemy(screen, (500,200),player, props,"Zombie")
Enemy3 = Enemy(screen, (600,200),player, props,"Fly")
props.append(Enemy1)
props.append(Enemy2)
props.append(Enemy3)
#fin de la création de toutes les instances
Entity = []

for i in props:
  try:
    if(i.EntityType):
      Entity.append(i)
  except:
    pass

img = pygame.image.load(os.path.join("assets/sprites/props", "Isaac's_Room_1.png")).convert_alpha()
image = pygame.transform.scale(img, (1920,1080))
RUNNING, PAUSE = 0, 1
state = RUNNING
pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r: state = PAUSE
            if e.key == pygame.K_e: state = RUNNING
    else:
        screen.fill((0,0,0))
        if state == RUNNING:

            screen.fill((0,0,0))

            screen.blit(image,(0,0))

            for Wall in props:
                Wall.Draw()

            player.update()
            
            for i in Entity:
                if(i.EntityType == "Enemy"):
                    if(i.hp <= 0): 
                        props.pop(props.index(i))
                        Entity.pop(Entity.index(i))

            screen.blit(update_fps(), (10,0))
            clock.tick(60)
            
            pygame.display.update()

        elif state == PAUSE:
            screen.blit(pause_text, (100, 100))

            pygame.display.flip()
            clock.tick(60)
        continue
    break
