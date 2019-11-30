import pygame, sys
from pygame.locals import *

TIMER = 30
SCREEN_X = 400
SCREEN_Y = 400

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
clock = pygame.time.Clock() #tick-tock

ending = button1 = button2 = False

corner1 = (28,18)  #Top Left corner of button 1
corner2 = (156,18)  #Top Left corner of button 2

image_length = 100 #length of the buttons
image_height = 100 #height of the buttons

counter = 0
sec =0 # 타이머(1초에 1씩 증가해서 출력)
time_limit = 60 # 제한 시간

BLACK=(0,0,0)
WHITE=(255,255,255)

class Player(object):
    def __init__(self):
        self.x1 = corner1[0]
        self.y1 = corner1[1]
        self.image1 = pygame.image.load("MR1.png").convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (image_length, image_height))

        self.x2 = corner2[0]
        self.y2 = corner2[1]
        self.image2 = pygame.image.load("MR2.png").convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (image_length, image_height))



    def draw(self):
        screen.blit(self.image1, (self.x1, self.y1))
        screen.blit(self.image2, (self.x2, self.y2))


player = Player()
player.draw()
pygame.display.update()

#Main Loop:
while ending==False:
    counter+=1
    clock.tick(TIMER)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ending=True # Time to leave
                print("Game Stopped Early by user")

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if (mouse_x > corner1[0]) and (mouse_x < corner1[0]+image_length) and (mouse_y > corner1[1]) and (mouse_y < corner1[1]+image_height):
                    if button2 == True:
                        screen.fill(BLACK)
                        newcharacter1 = pygame.image.load("MR5.png").convert_alpha()
                        newcharacter1 = pygame.transform.scale(newcharacter1, (image_length, image_height))
                        screen.blit(newcharacter1, ((corner1[0]+corner2[0])/2,(corner1[0]+corner2[1])/2))
                        image_length = 0
                        image_height = 0
                        pygame.display.update()

                    print ("character one is selected")
                    button1 = True
                    button2=False

                elif (mouse_x > corner2[0]) and (mouse_x < corner2[0]+image_length) and (mouse_y > corner2[1]) and (mouse_y < corner2[1]+image_height):
                    if button1 == True:
                        screen.fill(BLACK)

                        newcharacter2 = pygame.image.load("MR5.png").convert_alpha()
                        newcharacter2 = pygame.transform.scale(newcharacter2, (image_length, image_height))
                        screen.blit(newcharacter2, ((corner1[0] + corner2[0]) / 2, (corner1[0] + corner2[1]) / 2))
                        image_length = 0
                        image_height = 0
                        pygame.display.update()
                    button2 = True
                    print ("character two is selected")
                    # if(button1 == True and button2 == True):
                    #     screen.fill(BLACK)
                    button1=False


                else:
                    #print ("That's not a character")
                    button1=False
                    button2=False

    if counter == TIMER:  #prints the statements once a second
        counter=0
        print("%.2f" % sec)
        sec = sec +1
        #if button1==True:
           # print ("character one is currently selected")

        #elif button2==True:
         #   print ("character two is currently selected")

        #else:
            #print ("No character currently selected")

