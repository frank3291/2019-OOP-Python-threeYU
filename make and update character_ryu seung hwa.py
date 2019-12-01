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

while (True):
    counter+=1
    clock.tick(TIMER)
    cnt_checked_character = 0
    for i in range(4):
        for j in range(4):
            if character_checked[i][j] == 1:
                cnt_checked_character = cnt_checked_character +1

    flag=1
    if counter%500 == 0:
        best_character = 0
        for i in range(4):
            for j in range(4):
                if best_character < is_image[i][j]:
                    best_character = is_image[i][j]
        print(best_character)

        for i in range(4):
            for j in range(4):
                if is_image[i][j] == -1 and flag == 1:
                    screen.blit(maze_runner_character_image[0],(j*100, i*100))
                    is_image[i][j] = 0
                    pygame.display.update()
                    flag=0
            if flag == 0:
                break

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ending=True # Time to leave
                print("Game Stopped Early by user")

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos

                for i in range(4):
                    for j in range(4):
                        if is_image[i][j] != -1 and mouse_x > range_check[j] and mouse_x < range_check[j+1] and mouse_y > range_check[i] and mouse_y < range_check[i+1] and character_checked[i][j] == 0 and is_image[i][j] < 9 and cnt_checked_character < 2:
                            #print("click")
                            screen.blit(check, (range_check[j], range_check[i]))
                            pygame.display.update()
                            character_checked[i][j] = 1
                            cnt_checked_character = cnt_checked_character + 1
                            update_character()

                        elif is_image[i][j] != -1 and mouse_x > range_check[j] and mouse_x < range_check[j+1] and mouse_y > range_check[i] and mouse_y < range_check[i+1] and character_checked[i][j] == 1:
                            character_checked[i][j] = 0
                            cnt_checked_character = cnt_checked_character - 1
                            screen.blit(maze_runner_character_image[is_image[i][j]], (range_check[j], range_check[i]))
                            pygame.display.update()
                            update_character()