import pygame

SCREEN_X = 400
SCREEN_Y = 400
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))


a=[0,0,0,0,0,0,0,0,0,0]
a[0]=pygame.image.load("MR1.png").convert_alpha()
a[0]=pygame.transform.scale(a[0],(100,100))
screen.blit(a[0],(0,0))
pygame.display.update()
