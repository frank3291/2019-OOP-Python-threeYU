import pygame, sys
from pygame.locals import *
import time

TIMER = 300
clock = pygame.time.Clock() #tick-tock

counter = 0

BLACK = (0,0,0)
WHITE = (255,255,255)

maze_runner_character_image = [0,0,0,0,0,0,0,0,0,0]
is_image = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
character_checked = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]


maze_runner_character_image[0] = pygame.image.load("MR1.png").convert_alpha()
maze_runner_character_image[1] = pygame.image.load("MR2.png").convert_alpha()
maze_runner_character_image[2] = pygame.image.load("MR3.png").convert_alpha()
maze_runner_character_image[3] = pygame.image.load("MR4.png").convert_alpha()
maze_runner_character_image[4] = pygame.image.load("MR5.png").convert_alpha()
maze_runner_character_image[5] = pygame.image.load("MR6.png").convert_alpha()
maze_runner_character_image[6] = pygame.image.load("MR7.png").convert_alpha()
maze_runner_character_image[7] = pygame.image.load("MR8.png").convert_alpha()
maze_runner_character_image[8] = pygame.image.load("MR9.png").convert_alpha()
maze_runner_character_image[9] = pygame.image.load("MR10.png").convert_alpha()


for i in range(10):
    maze_runner_character_image[i] = pygame.transform.scale(maze_runner_character_image[i], (100, 100))

image_delete = pygame.image.load("black.png").convert_alpha()
image_delete = pygame.transform.scale(image_delete,(100,100))

check = pygame.image.load("check.png").convert_alpha()
check = pygame.transform.scale(check, (100,100))

range_check = [0, 100, 200, 300, 400]

def update_character():
    for k in range(4):
        for l in range(4):
            if character_checked[k][l] == 1 and not (k == i and l == j) and is_image[k][l] == is_image[i][j]:
                screen.blit(image_delete, (j * 100, i * 100))
                screen.blit(image_delete, (l * 100, k * 100))
                character_checked[i][j] = 0
                character_checked[k][l] = 0
                screen.blit(maze_runner_character_image[is_image[i][j] + 1], (l * 100, k * 100))
                is_image[k][l] = is_image[k][l] + 1
                is_image[i][j] = - 1

                pygame.display.update()