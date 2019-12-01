#수정 1. 타이머 기능 추가
#수정 2. 배경음악, 캐릭터 정보창 추가
#수정 3. 몬스터 추가
# Maze
import random, pygame, sys
import time
import numpy as np
from pygame.locals import *
#IMAGE PART
timerimg=pygame.image.load("timer.png")
timerimg=pygame.transform.scale(timerimg,(360,180))
infoimg=pygame.image.load("information.png")
infoimg=pygame.transform.scale(infoimg,(225,177))
A_1=pygame.image.load("A_1.png")
A_1=pygame.transform.scale(A_1,(142,156))
A_2=pygame.image.load("A_2.png")
A_2=pygame.transform.scale(A_2,(142,156))
A_3=pygame.image.load("A_3.png")
A_3=pygame.transform.scale(A_3,(142,156))
B_1=pygame.image.load("B_1.png")
B_1=pygame.transform.scale(B_1,(142,156))
B_2=pygame.image.load("B_2.png")
B_2=pygame.transform.scale(B_2,(142,156))
B_3=pygame.image.load("B_3.png")
B_3=pygame.transform.scale(B_3,(142,156))
C_1=pygame.image.load("C_1.png")
C_1=pygame.transform.scale(C_1,(142,156))
C_2=pygame.image.load("C_2.png")
C_2=pygame.transform.scale(C_2,(142,156))
C_3=pygame.image.load("C_3.png")
C_3=pygame.transform.scale(C_3,(142,156))
S_1=pygame.image.load("S_1.png")
S_1=pygame.transform.scale(S_1,(142,156))

#setting part
playerdata={'Name':'frank','rank':'A','count':10}
playerimage=A_2
pygame.init()
FPS = 15
WINDOWWIDTH = 600
WINDOWHEIGHT = 780
global w, h
w = 40
h = 40
CELLSIZE = WINDOWWIDTH // w
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

youwin=pygame.image.load("youwin.jpg")
youwin=pygame.transform.scale(youwin,(400,300))
youlose=pygame.image.load("youlose.jpg")
youlose=pygame.transform.scale(youlose,(400,300))
#color part
#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE=(0,0,255)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK
#줄임말
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
#text
timertext=pygame.font.SysFont('freesansbold.ttf', 150)
normaltext = pygame.font.SysFont('freesansbold.ttf', 24)
#flag
endgame=False
def terminate(endgame):
    if endgame:
        return 1
    return 0

def getRandomLocation(x,y):
    ans={'x': random.randint(7, x-1), 'y': random.randint(7, y - 1)}
    return ans

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('[Press Any Button].', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def InputImage(x,y,IMG):
    DISPLAYSURF.blit(IMG,(x,y))

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate(False)

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate(False)
    return keyUpEvents[0].key


def showGameOverScreen(tmp):
    DISPLAYSURF.fill(BGCOLOR)
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render('YOU', True, WHITE)
    if tmp==1:
        overSurf = gameOverFont.render('WIN!', True, GREEN)
        InputImage(100, 300, youwin)
    elif tmp==0:
        overSurf = gameOverFont.render('LOSE!', True, RED)
        InputImage(100, 300, youlose)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(1000)
    return


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('MazeRunner!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('MazeRunner!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


def drawGoal(x, y):
    gx = x * CELLSIZE
    gy = y * CELLSIZE
    goalRect = pygame.Rect(gx, gy, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, goalRect)

class creature:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def drawself(self,color):
        x = self.x * CELLSIZE
        y = self.y * CELLSIZE
        playerRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF,color, playerRect)

class Monster(creature):
    def __init__(self,x,y):
        super().__init__(x,y);
        self.color=BLUE
        self.nextloc=[0,0]
        self.movex=[1,-1,0,0]
        self.movey=[0,0,-1,1]

    def lengthwithhuman(self,humanx,humany,x,y):
        return (humanx-x)**2+(humany-y)**2

    def movement(self,humanx,humany,maze):
        min=1000000
        for i in range(4):
            monx=self.x+self.movex[i]
            mony=self.y+self.movey[i]
            if min>self.lengthwithhuman(humanx,humany,monx,mony) and monx<w and monx>=0 and mony<h and mony>=0:
                min = self.lengthwithhuman(humanx, humany,monx,mony)
                self.nextloc[0]=self.x+self.movex[i]
                self.nextloc[1]=self.y+self.movey[i]
        return self.nextloc

class Player(creature):
    def __init__(self,x,y,name,rank,count):
        super().__init__(x,y)
        self.color=GREEN
        self.information={'rank':rank,'Name':name,'count':count}

    def moveRight(self):
        self.x = self.x + 1
    def moveLeft(self):
        self.x = self.x - 1

    def moveUp(self):
        self.y = self.y - 1

    def moveDown(self):
        self.y = self.y + 1

    def charinfo(self):
        textname = normaltext.render("NAME", True, BLACK)
        textrank = normaltext.render("RANK", True, BLACK)
        textcount = normaltext.render("COUNT", True, BLACK)
        textname_val = normaltext.render(self.information['Name'], True, BLUE)
        textrank_val = normaltext.render(self.information['rank'], True, BLUE)
        textcount_val = normaltext.render("%s"%(self.information['count']), True, BLUE)
        DISPLAYSURF.blit(textname, (530, 621))
        DISPLAYSURF.blit(textrank, (530, 663))
        DISPLAYSURF.blit(textcount, (530, 705))
        DISPLAYSURF.blit(textname_val, (530, 642))
        DISPLAYSURF.blit(textrank_val, (530, 684))
        DISPLAYSURF.blit(textcount_val, (530, 726))

class background:
    def __init__(self):
        self.level={'C':20,'B':30,'A':40,'S':40}
        self.M = w
        self.N = h
        self.maze = []

    def mazemaker(self):
        Map = np.ndarray([w, h, 2], np.int)
        Map[::] = -1
        current = [0, 0]  # 현재 칸. 초기값은 시작점을 뜻한다. 예컨대 [w/2,h/2]로 설정하면 중간에서부터 미로를 만든다.
        visited = []
        while True:
            Map[0, 0, :] = 0
            current = self.go_next(current, Map, visited)
            if current == None:
                break
        mazemap = self.drawMap(Map)
        return mazemap

    def random_select(self,arr):
        return arr[random.randint(0, len(arr) - 1)]

    def get_around(self,cur, map):
        next = []
        h = map.shape[0]
        w = map.shape[1]
        if cur[0] > 0 and map[cur[0] - 1, cur[1]][0] < 0: next.append([cur[0] - 1, cur[1]])
        if cur[0] < h - 1 and map[cur[0] + 1, cur[1]][0] < 0: next.append([cur[0] + 1, cur[1]])
        if cur[1] > 0 and map[cur[0], cur[1] - 1][0] < 0: next.append([cur[0], cur[1] - 1])
        if cur[1] < w - 1 and map[cur[0], cur[1] + 1][0] < 0: next.append([cur[0], cur[1] + 1])
        return next

    def go_next(self,cur, map, visited):
        nexts = self.get_around(cur, map)
        if len(nexts) > 0:  # 만약 다음에 갈 곳이 있으면
            visited.append(cur)  # visited 배열에 현재 좌표를 추가하고
            next = self.random_select(nexts)  # 주변의 칸 중 이동할 칸을 정한다.
            map[next[0], next[1]] = cur  # 이동할 칸에 현재 칸의 좌표를 적는다.
            return next  # 이동할 칸을 반환한다.
        else:  # 만약 갈 곳이 없으면
            # visited 배열에서 현재 칸의 좌표를 지운다.
            if cur in visited:
                visited.remove(cur)
            # 만약 visited 배열이 비었으면,
            # 이 상태는 여태까지 방문했던 모든 칸들에 대해서, 사방이 전부 한 번 이상 방문했던 칸이라는 뜻이다.
            # 즉, 맵의 모든 칸들을 전부 다 방문하였다.
            if len(visited) == 0:
                return None  # 따라서 None 을 반환하여 마지막 칸을 방문했음을 알린다.
            return self.random_select(visited)  # 만약 visited 배열이 안 비었으면 visited 배열 중 아무 칸을 반환한다.

    def drawMap(self,map):
        h = map.shape[0] * 2 - 1
        w = map.shape[1] * 2 - 1
        draw = np.ndarray([w, h], np.int)
        draw[::] = 0

        for y in range(map.shape[0]):
            for x in range(map.shape[1]):
                pos = map[y, x]
                draw[y * 2, x * 2] = 1
                draw[pos[0] * 2, pos[1] * 2] = 1
                draw[y + pos[0], x + pos[1]] = 1

        return draw

    def draw(self):
        for i in range(self.N):
            for j in range(self.M):
                y = i * CELLSIZE
                x = j * CELLSIZE
                if self.maze[i][j] == 0:
                    wallRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
                    pygame.draw.rect(DISPLAYSURF, WHITE, wallRect)

    def drawbackground(self,IMG1,IMG2,time):
        InputImage(6, 606, IMG1)
        InputImage(372, 609, IMG2)
        texttime = timertext.render(time, True, BLACK)
        DISPLAYSURF.blit(texttime, (21, 630))

def main(playerdata,playerimage): #playerdata={name,rank}
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('MAZE')
    showStartScreen()
    tmp=runGame(playerdata,playerimage)
    showGameOverScreen(tmp)
    if tmp==1:
        return terminate(True)
    else:
        return terminate(False)

def runGame(playerdata,playerimage):
    pygame.mixer.music.load('bgmusic.mp3')
    pygame.mixer.music.play(-1,0.0)
    bg=background()
    human = Player(0,0,playerdata['Name'],playerdata['rank'],playerdata['count'])
    bg.M=bg.level[human.information['rank']]
    Time=bg.M
    bg.N=bg.level[human.information['rank']]
    global CELLSIZE,CELLHEIGHT,CELLWIDTH,WINDOWWIDTH
    w=bg.M
    h=bg.N
    CELLSIZE=WINDOWWIDTH//bg.M
    CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
    CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
    bg.maze=bg.mazemaker()
    bg.maze[w-1][h-1]=1
    monnum=0
    monsters = []
    if human.information['rank']=='S':
        monnum=4
    elif human.information['rank']=='A':
        monnum=3
    elif human.information['rank']=='B':
        monnum=2
    elif human.information['rank']=='C':
        monnum=1

    for i in range(monnum):
        loc=getRandomLocation(w,h)
        x=loc['x']
        y = loc['y']
        greeber=Monster(x,y)
        monsters.append(greeber)

    pygame.time.wait(1000)
    mouse_x=0
    mouse_y=0
    start_ticks=pygame.time.get_ticks()
    flag=False
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        timeleft=Time-seconds
        if timeleft<0:
            return 0
        sec=int(timeleft//1)
        smallsec=int(round(timeleft%1,2)//0.01)
        timerstr=str(sec)+' : '+str(smallsec)
        nowx = human.x
        nowy = human.y
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate(False)
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and nowx - 1 >= 0 and bg.maze[nowy][nowx - 1] == 1:
                    human.moveLeft()
                elif (event.key == K_RIGHT or event.key == K_d) and nowx + 1 < bg.M and bg.maze[nowy][nowx + 1] == 1:
                    human.moveRight()
                elif (event.key == K_UP or event.key == K_w) and nowy - 1 >= 0 and bg.maze[nowy - 1][nowx] == 1:
                    human.moveUp()
                elif (event.key == K_DOWN or event.key == K_s) and nowy + 1 < bg.N and bg.maze[nowy + 1][nowx] == 1:
                    human.moveDown()
                elif event.key == K_ESCAPE:
                    terminate(False)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                mapx = mouse_x // CELLSIZE
                mapy = mouse_y // CELLSIZE
                if human.information['count'] > 0:
                    bg.maze[mapy][mapx] = 1
                    human.information['count'] = human.information['count'] - 1

        if nowx == w - 1 and nowy == h - 1:
            return 1
        for i in range(monnum):
             if monsters[i].x==nowx and monsters[i].y==nowy:
                return 0

        if smallsec%6==0:
            for i in range(monnum):
                greeber=monsters[i]
                next=greeber.movement(nowx,nowy,bg.maze)
                greeber.x=next[0]
                greeber.y=next[1]
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        bg.draw()
        bg.drawbackground(timerimg, infoimg, timerstr)
        human.charinfo()
        drawGoal(w - 1, h - 1)
        human.drawself(human.color)
        InputImage(378,621,playerimage)
        for i in range(monnum):
            greeber=monsters[i]
            greeber.drawself(greeber.color)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    print(main(playerdata,playerimage))