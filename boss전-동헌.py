import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 1500
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
#
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey(endgame):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN and event.type!=K_SPACE:
                if event.key == K_ESCAPE or endgame :
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def makehotspot(IMG,screen):
    loc=getRandomLocation()
    screen.blit(IMG,loc)
    return loc

def getRandomLocation():
    return [random.randint(100, WINDOWWIDTH - 100), random.randint(100, WINDOWHEIGHT - 100)]

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('BOSS')
pygame.mouse.set_visible(False)
def touchhotspot(hotspot):
    if playerRect.colliderect(hotspot['rect']):
        return True
    return False

font = pygame.font.SysFont(None, 48)
fontnormal = pygame.font.SysFont(None,30)
def showbosshp(hp,screen):
    if hp<=0:
        hp=0
    drawText('boss | wikid', fontnormal, windowSurface, 250,35)
    pygame.draw.rect(screen,(255,0,0),(250,20,hp,10))

def drawuserhp(hp,screen):
    drawText('HP', fontnormal, windowSurface, 1450,560)
    pygame.draw.rect(screen,(0,255,0),(1450,550,20,-hp))


pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1,0.0)


playerImage = pygame.image.load('player.png')
playerImage=pygame.transform.scale(playerImage,(20,20))

playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')
hotspotImage =pygame.image.load('hotspot.jpg')
hotspotImage = pygame.transform.scale(hotspotImage,(40,40))
drawText('BOSS', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey(False)

topScore = 0
while True:
    cnt=0
    baddies = []
    hotspot={'rect':[0,0,0,0]}
    flag=True
    endgame=False
    firsttime = True
    score = 0
    hp=1000
    userhp=300
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    Levelcount=0
    start_ticks = pygame.time.get_ticks()
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        score += 1
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if hp <= 0:
                        cnt += 1
            if touchhotspot(hotspot):
                if event.type==KEYDOWN:
                    if event.key==K_SPACE:
                        if hp<=0:
                            cnt+=1
                        hotspot['hp']-=100;
                        if hotspot['hp']<0:
                            flag=True
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            #if event.type == MOUSEMOTION:
                #playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)


        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        windowSurface.fill(BACKGROUNDCOLOR)
        drawuserhp(userhp,windowSurface)
        if flag:
            if hp>0:
                hp-=80
            Levelcount+=1
            BADDIEMINSPEED +=2
            BADDIEMAXSPEED +=2
            PLAYERMOVERATE +=1
            flag=False
            loc=makehotspot(hotspotImage, windowSurface)
            x=loc[0]
            y=loc[1]
            hotspot={'rect':pygame.Rect(x, y, 100, 100),'hp':random.randint(Levelcount*40,Levelcount*80)}
        print(Levelcount)
        windowSurface.blit(hotspotImage,(x,y))
        drawText("%s"% (hotspot['hp']),font,windowSurface,x,y-20)
        showbosshp(hp,windowSurface)

        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        windowSurface.blit(playerImage, playerRect)

        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        if playerHasHitBaddie(playerRect, baddies) :
            print("chk")
            userhp-=5*Levelcount//2
            if userhp<=0:
                break
            if score > topScore:
                topScore = score
        if hp<=0:
            if firsttime:
                print("chk")
                firsttime=False
                nowtime=seconds
            timeleft=10-(seconds-nowtime)//1
            text1=font.render('PRESS SPACE!!  MORE THAN 80!!!!!!',True,(255,0,0))
            text2=font.render('%s' % (cnt), True,(255,0,0))
            text3=font.render('%s' % (timeleft),True,(255,0,0))
            windowSurface.blit(text1,((WINDOWWIDTH/2)-200, (WINDOWHEIGHT/2)-50))
            windowSurface.blit(text2,((WINDOWWIDTH/2)-150, (WINDOWHEIGHT/2)))
            windowSurface.blit(text3,((WINDOWWIDTH/2)-150,(WINDOWHEIGHT/2)+50))
            if timeleft<=0:
                if cnt<80:
                    userhp=-10
                    break
                if cnt>80:
                    break

        pygame.display.update()
        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    if userhp<=0:
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText('You Lose!! ', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        endgame=True
    if hp<=0:
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText('You WIN!! THE END', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
        endgame=True
    drawText('Press a key to go menu.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey(endgame)

