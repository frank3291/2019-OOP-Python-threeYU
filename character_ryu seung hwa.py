import pygame, sys
from pygame.locals import *
import time

TIMER = 300
SCREEN_X = 400
SCREEN_Y = 400

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
clock = pygame.time.Clock() #tick-tock

ending = button1 = button2 = False

counter = 0
sec =0 # 타이머(1초에 1씩 증가해서 출력)
time_limit = 60 # 제한 시간

BLACK=(0,0,0)
WHITE=(255,255,255)
pygame.init()
# corner = [[0,0],[100,0],[200,0],[300,0],[0,100],[100,100],[200,100],[300,100],[0,200],[100,200],[200,200],[300,200],[0,300],[100,300],[200,300],[300,300]]
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



while (True):

    counter+=1
    clock.tick(TIMER)
    flag=1
    if counter%500 == 0:
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
                        if is_image[i][j] != -1 and mouse_x > range_check[j] and mouse_x < range_check[j+1] and mouse_y > range_check[i] and mouse_y < range_check[i+1]:
                            #print("click")
                            screen.blit(check, (range_check[j], range_check[i]))
                            pygame.display.update()
                            character_checked[i][j] = 1

                            for k in range(4):
                               for l in range(4):
                                    if character_checked[k][l]==1 and k!=i and l!=j and is_image[k][l] == is_image[i][j]:
                                        screen.blit(image_delete,(j*100,i*100))
                                        screen.blit(image_delete,(l*100,k*100))
                                        character_checked[i][j] = 0
                                        character_checked[k][l] = 0
                                        screen.blit(maze_runner_character_image[is_image[i][j]+1],(min(j,l)*100, min(i,k)*100))
                                        is_image[min(i,k)][min(j,l)]=is_image[i][j]+1

                                        is_image[i][j] = -1
                                        is_image[k][l] = -1
                                        pygame.display.update()





    #Main Loop:
# while ending==False:
#
#     counter+=1
#     clock.tick(TIMER)
#
#     for event in pygame.event.get():
#         if event.type == KEYDOWN:
#             if event.key == K_ESCAPE:
#                 ending=True # Time to leave
#                 print("Game Stopped Early by user")
#
#         elif event.type == MOUSEBUTTONDOWN:
#
#             if event.button == 1:
#                 mouse_x, mouse_y = event.pos
#                 if (mouse_x > corner[0][0]) and (mouse_x < corner[0][0]+image_length) and (mouse_y > corner[0][1]) and (mouse_y < corner[0][1]+image_height):
#                     print("character one is selected")
#                     check_image1()
#                     if button2 == True:
#                         time.sleep(1)
#                         #screen.fill(BLACK)
#                         screen.blit(image_delete,(corner[0][0], corner[0][1]))
#                         screen.blit(image_delete,(corner[1][0], corner[1][1]))
#
#                         newcharacter1 = pygame.image.load("MR4.png").convert_alpha()
#                         newcharacter1 = pygame.transform.scale(newcharacter1, (image_length, image_height))
#                         screen.blit(newcharacter1, (min(corner[0][0], corner[1][0]), min(corner[0][1], corner[1][1])))
#                         image_length = 0
#                         image_height = 0
#                         pygame.display.update()
#
#                     button1 = True
#                     button2 = False
#
#                 elif (mouse_x > corner[1][0]) and (mouse_x < corner[1][0]+image_length) and (mouse_y > corner[1][1]) and (mouse_y < corner[1][1]+image_height):
#
#                     print ("character two is selected")
#                     check_image2()
#
#                     if button1 == True:
#                         time.sleep(1)
#                         screen.fill(BLACK)
#                         newcharacter2 = pygame.image.load("MR4.png").convert_alpha()
#                         newcharacter2 = pygame.transform.scale(newcharacter2, (image_length, image_height))
#                         screen.blit(newcharacter2, (min(corner[0][0], corner[1][0]), min(corner[0][1], corner[1][1])))
#                         image_length = 0
#                         image_height = 0
#                         pygame.display.update()
#
#                     button2 = True
#                     button1 = False
#
#
#                 else:
#                     button1 = False
#                     button2 = False


    # if counter == TIMER:  #prints the statements once a second
    #
    #     counter=0
    #     print("%.2f" % sec)
    #     sec = sec +1
    #
    #     if sec%5 == 0:
    #         image_new = pygame.image.load("MR3.png").convert_alpha()
    #         image_new = pygame.transform.scale(image_new, (image_length, image_height))
    #         screen.blit(image_new, (200,0))
    #         pygame.display.update()


