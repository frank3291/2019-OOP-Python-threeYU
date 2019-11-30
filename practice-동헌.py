#수정 1. 타이머 기능 추가
#수정 2. 배경음악, 캐릭터 정보창 추가
#수정 3. 몬스터 추가
# Maze
import random, pygame, sys
import time
import numpy as np
from pygame.locals import *
#program setting
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
#character part

#IMAGE PART
timerimg=pygame.image.load("timer.png")
timerimg=pygame.transform.scale(timerimg,(360,180))
infoimg=pygame.image.load("information.png")
infoimg=pygame.transform.scale(infoimg,(225,177))
A_1=pygame.image.load("A_1.png")
A_1=pygame.transform.scale(A_1,(142,156))
youwin=pygame.image.load("youwin.jpg")
youwin=pygame.transform.scale(youwin,(400,300))
youlose=pygame.image.load("youlose.jpg")
youlose=pygame.transform.scale(youlose,(400,300))
#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE=(0,0,255)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class Monster:
    x=0
    y=0
    nextloc=[0,0]
    movex=[1,-1,0,0]
    movey=[0,0,-1,1]

    def lengthwithhuman(self,humanx,humany,mobx,moby):
        return (humanx-mobx)**2+(humany-moby)**2

    def movement(self,humanx,humany,mobx,moby,maze):
        min=1000000
        for i in range(4):
            monx=mobx+self.movex[i]
            mony=moby+self.movey[i]
            if min>self.lengthwithhuman(humanx,humany,monx,mony) and monx<w and monx>=0 and mony<h and mony>=0:
                min = self.lengthwithhuman(humanx, humany, monx, mony)
                self.nextloc[0]=mobx+self.movex[i]
                self.nextloc[1]=moby+self.movey[i]

        return self.nextloc

class Player:
    x = 0
    y = 0
    speed = 1
    rank="A"
    Name='Minho'
    count = 10

    def moveRight(self):
        self.x = self.x + self.speed

    def moveLeft(self):
        self.x = self.x - self.speed

    def moveUp(self):
        self.y = self.y - self.speed

    def moveDown(self):
        self.y = self.y + self.speed


class Maze:
    def __init__(self):
        self.M = w
        self.N = h
        self.maze = []

    def draw(self):
        for i in range(self.N):
            for j in range(self.M):
                y = i * CELLSIZE
                x = j * CELLSIZE
                if self.maze[i][j] == 0:
                    wallRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
                    pygame.draw.rect(DISPLAYSURF, WHITE, wallRect)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, breaksound
    global item
    item = getRandomLocation()
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('MAZE')

    showStartScreen()

    tmp=runGame()
    showGameOverScreen(tmp)
    terminate()

def mazemaker():
    Map = np.ndarray([w, h, 2], np.int)
    Map[::] = -1
    current = [0, 0]  # 현재 칸. 초기값은 시작점을 뜻한다. 예컨대 [w/2,h/2]로 설정하면 중간에서부터 미로를 만든다.
    visited = []
    while True:
        Map[0, 0, :] = 0
        current = go_next(current, Map, visited)
        if current == None:
            break
    mazemap = drawMap(Map)
    return mazemap


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    ans={'x':0,'y':0}
    while ans['x']<10 and ans['y']<10:
        ans={'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

    return ans

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('[Press Any Button].', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def InputImage(x,y,IMG):
    DISPLAYSURF.blit(IMG,(x,y))


def runGame():
    pygame.mixer.music.load('bgmusic.mp3')
    pygame.mixer.music.play(-1,0.0)

    mazemap = mazemaker()
    human = Player()
    monster=Monster()
    monloc=getRandomLocation()
    monster.x=monloc['x']
    mobx=monster.x
    monster.y=monloc['y']
    moby=monster.y
    field = Maze()
    field.maze = mazemap
    field.maze[w - 1][h - 1] = 1
    garo = w
    sero = h
    mouse_x=0
    mouse_y=0
    nowx=0
    nowy=0
    start_ticks=pygame.time.get_ticks()
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        timeleft=40-seconds
        if timeleft<0:
            return 0
        sec=int(timeleft//1)
        secchk=sec%2
        smallsec=int(round(timeleft%1,2)//0.01)
        smallsecchk=smallsec%4
        timerstr=str(sec)+' : '+str(smallsec)
        timertext=pygame.font.SysFont('freesansbold.ttf', 150)
        normaltext = pygame.font.SysFont('freesansbold.ttf', 24)
        texttime=timertext.render(timerstr,True,BLACK)
        textname=normaltext.render("NAME",True,BLACK)
        textrank=normaltext.render("RANK",True,BLACK)
        textcount=normaltext.render("COUNT",True,BLACK)
        textname_val = normaltext.render(human.Name, True, BLUE)
        textrank_val = normaltext.render(human.rank, True, BLUE)
        textcount_val = normaltext.render(str(human.count), True, BLUE)
        for event in pygame.event.get():
            nowx = human.x
            nowy = human.y
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and nowx - 1 >= 0 and field.maze[nowy][nowx - 1] == 1:
                    human.moveLeft()
                elif (event.key == K_RIGHT or event.key == K_d) and nowx + 1 < garo and field.maze[nowy][nowx + 1] == 1:
                    human.moveRight()
                elif (event.key == K_UP or event.key == K_w) and nowy - 1 >= 0 and field.maze[nowy - 1][nowx] == 1:
                    human.moveUp()
                elif (event.key == K_DOWN or event.key == K_s) and nowy + 1 < sero and field.maze[nowy + 1][nowx] == 1:
                    human.moveDown()
                elif event.key == K_ESCAPE:
                    terminate()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x = pos[0]
                mouse_y = pos[1]
                print(pos)
                mapx = mouse_x // CELLSIZE
                mapy = mouse_y // CELLSIZE
                if human.count > 0:
                    field.maze[mapy][mapx] = 1
                    human.count = human.count - 1
                    print(human.count)

            if nowx == w - 1 and nowy == h - 1:
                return 1
            if mobx==nowx and moby==nowy:
                return 0
        if secchk==0 and smallsecchk==0:
            nextloc=monster.movement(nowx,nowy,mobx,moby,field.maze)
            mobx=nextloc[0]
            moby=nextloc[1]
        DISPLAYSURF.fill(BGCOLOR)
        field.draw()
        drawGrid()
        InputImage(6, 606, timerimg)
        InputImage(372,609,infoimg)
        InputImage(378,621,A_1)
        DISPLAYSURF.blit(texttime, (21, 630))
        DISPLAYSURF.blit(textname, (530, 621))
        DISPLAYSURF.blit(textrank, (530, 663))
        DISPLAYSURF.blit(textcount, (530, 705))
        DISPLAYSURF.blit(textname_val, (530, 642))
        DISPLAYSURF.blit(textrank_val, (530, 684))
        DISPLAYSURF.blit(textcount_val, (530, 726))
        drawGoal(w - 1, h - 1)
        drawPlayer(nowx, nowy)
        drawmonster(mobx,moby)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
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


def drawPlayer(nowx, nowy):
    x = nowx * CELLSIZE
    y = nowy * CELLSIZE
    playerRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, DARKGREEN, playerRect)

def drawmonster(nowx, nowy):
    x = nowx * CELLSIZE
    y = nowy * CELLSIZE
    playerRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, BLUE, playerRect)


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


# mazemaker
def random_select(arr):
    return arr[random.randint(0, len(arr) - 1)]


def get_around(cur, map):
    next = []
    h = map.shape[0]
    w = map.shape[1]
    if cur[0] > 0 and map[cur[0] - 1, cur[1]][0] < 0: next.append([cur[0] - 1, cur[1]])
    if cur[0] < h - 1 and map[cur[0] + 1, cur[1]][0] < 0: next.append([cur[0] + 1, cur[1]])
    if cur[1] > 0 and map[cur[0], cur[1] - 1][0] < 0: next.append([cur[0], cur[1] - 1])
    if cur[1] < w - 1 and map[cur[0], cur[1] + 1][0] < 0: next.append([cur[0], cur[1] + 1])
    return next


def go_next(cur, map, visited):
    nexts = get_around(cur, map)
    if len(nexts) > 0:  # 만약 다음에 갈 곳이 있으면
        visited.append(cur)  # visited 배열에 현재 좌표를 추가하고
        next = random_select(nexts)  # 주변의 칸 중 이동할 칸을 정한다.
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
        return random_select(visited)  # 만약 visited 배열이 안 비었으면 visited 배열 중 아무 칸을 반환한다.


# 본 프로그램에서 다루는 맵은 각 칸에 그 이전 칸의 정보가 담겨있다.
# 이를 시각적으로 볼 수 있도록 변환하는 메서드.
# 맵의 크기를 2배로 늘린 뒤, 각 칸과, 각 칸의 이전 칸,그리고 그 사이를 1로 한다.
# 그리고 나머지는 0으로 한다.
# 이렇게 하면 벽을 0으로, 경로를 1로 표시한 2차원 배열이 나온다.
def drawMap(map):
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


if __name__ == '__main__':
    main()