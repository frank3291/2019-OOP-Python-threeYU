import pygame, sys
def main():
    while True:
        runGame()

def terminate():
    pygame.quit()
    sys.exit()

def runGame():
    startx=0
    starty=0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

