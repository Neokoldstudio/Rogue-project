#####################################################################
import pygame
import os         #modules à importer
import sys
#####################################################################
from assets.objects.Player import Player
from assets.objects.enemies.Enemies import Enemy     #import des objets créés (ennemis, murs, joueur, ...)
from assets.objects.environnement.Wall import Wall
from assets.objects.environnement.InvisibleWall import InvisibleWall
from assets.objects.healthBar import Health
from assets.objects.environnement.heart import Heart
#####################################################################

pygame.init()

#screen_width, screen_height = 1000,1000

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)#affichage en plein écran
#screen = pygame.display.set_mode((600, 600))#affiche dans une fenêtre de 600 par 600

pygame.display.set_caption("Rogue Like")

running = True
clock = pygame.time.Clock()#création d'une clock gérant le nombre d'image par seconde
font = pygame.font.SysFont("Arial", 18)
 
 
def update_fps():#fonction permettant d'afficher le nombre d'images par secondes atteintes par le jeu

	fps = str(int(clock.get_fps()))

	fps_text = font.render(fps, 1, pygame.Color("green"))
	return fps_text#retourne un texte ( objet de pygame )


#création de toutes les instances des objets 
props = []

IWallTop = InvisibleWall(screen, (0, 180), (1920,2))   #-
IWallLeft = InvisibleWall(screen, (200, 0), (2,1080))  # |
IWallRight = InvisibleWall(screen, (1718, 0), (2,1080))# |-- création des murs
IWallDown = InvisibleWall(screen, (0, 888), (1920,2))  # |
wall = Wall(screen, "wall.jpg", (600,150),(150,150))   #-

props = [IWallTop, IWallLeft, IWallRight, IWallDown, wall]#liste contenant tout les objets avec lesquels le joueur peut entrer en collision

player = Player(screen, "test_idle.png", (1000,100),props)


Enemy1 = Enemy(screen, (300,200),player, props,"Fly")   #-
Enemy2 = Enemy(screen, (500,200),player, props,"Zombie")# |-- création des ennemis
Enemy3 = Enemy(screen, (600,200),player, props,"Fly")   #-
heart = Heart(screen, (500,500), player)
props.append(heart)
props.append(Enemy1)
props.append(Enemy2)
props.append(Enemy3)


healthBar = Health(screen, (200,100), player)#création de l'objet healthbar

#fin de la création de toutes les instances
Entity = []

for i in props: #isole les "entitées" des murs, afin de créer une liste référençant seulement les entitées ( ennemies, etc ... )
  try:
    if(i.EntityType): #si la variable EntityType est présente en tant qu'argument de l'objet, on le rajoute dans la liste
      Entity.append(i)
  except:
    pass

img = pygame.image.load(os.path.join("assets/sprites/props", "Isaac's_Room_1.png")).convert_alpha()#chargement de l'imgage de fond 
image = pygame.transform.scale(img, (1920,1080))#rescale l'image
RUNNING, PAUSE = 0, 1 #on associe à RUNNING et PAUSE les valeurs 0 et 1, question de lisibilitée
state = RUNNING
pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))

while running:#boucle principale, exécutée ~60 fois par secondes ( la clock permet de définir le nombre d'exécution )
    for e in pygame.event.get():#event listener, permettant de récupèrer l'appuis sûr des touches
        if e.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:#condition permettant de quitter le jeu
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r: state = PAUSE#la variable state 
            if e.key == pygame.K_e: state = RUNNING
    else:
        screen.fill((0,0,0))
        if state == RUNNING:#le jeu est en état "jouable"

            #screen.fill((0,0,0))

            screen.blit(image,(0,0))#affiche l'image de fond

            for Prop in props:
                Prop.Draw()

            player.update()
            
            for i in Entity: #bout de code gérant la mort des ennemis 
                if(i.EntityType == "Enemy"):
                    if(i.hp <= 0): 
                        props.pop(props.index(i))
                        Entity.pop(Entity.index(i))
                if(i.EntityType == "heart"):
                    if(i.used):
                        props.pop(props.index(i))
                        Entity.pop(Entity.index(i))

            healthBar.Update()

            screen.blit(update_fps(), (10,0))

            clock.tick(60)#le nombre maximal d'images par seconde est 60 fps
            
            pygame.display.update()#ligne permettant de rafraichir l'écran

        elif state == PAUSE:#le jeu est en pause
            screen.blit(pause_text, (100, 100))

            pygame.display.flip()
            clock.tick(60)
        continue
    break