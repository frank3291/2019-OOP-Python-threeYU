# 맨 처음 시작화면
import pygame as pg
import minigame
import boss
from Makecharater import *

dataforboss={0:[boss.C_3,'Chuck','C',3],1:[boss.C_1,'Winston','C',4],2:[boss.C_2,'Frypan','C',5],3:[boss.B_1,'Gally','B',7],4:[boss.B_2,'Alby','B',8],5:[boss.B_3,'Branda','B',9],6:[boss.A_3,'Newt','A',10],7:[boss.A_2,'Teresa','A',11],8:[boss.A_1,'Minho','A',12],9:[boss.S_1,'Thomas','S',50]}
dataformini={0:[minigame.C_3,'Chuck','C',3],1:[minigame.C_1,'Winston','C',4],2:[minigame.C_2,'Frypan','C',5],3:[minigame.B_1,'Gally','B',7],4:[minigame.B_2,'Alby','B',8],5:[minigame.B_3,'Branda','B',9],6:[minigame.A_3,'Newt','A',10],7:[minigame.A_2,'Teresa','A',11],8:[minigame.A_1,'Minho','A',12],9:[minigame.S_1,'Thomas','S',50]}
playerdata={'Name':'thomas','rank':'S','count':15}
playerimage1 = minigame.S_1
playerimage2 = boss.S_1

pg.init()
counter = 0
F = 1
ticket = 0
fontnormal=pygame.font.SysFont('freesansbold.ttf',90)

best_character = 0
cnt_checked_character = 0
Background = pg.image.load("background.jpg")
Background = pg.transform.scale(Background,(1200,800))
Title = pg.image.load("Title.PNG")
Title = pg.transform.scale(Title,(900,250))
HowToPlayImg = pg.image.load("howtoplayimg.PNG")
HowToPlayImg = pg.transform.scale(HowToPlayImg,(1200,800))
GamePlayImg = pg.image.load("GamePlayIMG.png")
GamePlayImg = pg.transform.scale(GamePlayImg,(1200,800))
pg.mixer_music.load("backgroundmusic.mp3")
pg.mixer_music.play(-1,0.0)

screen = pg.display.set_mode((1200, 800))
FONT = pg.font.SysFont('Comic Sans MS', 32)

IMAGE_NORMAL = pg.Surface((100, 32))
IMAGE_NORMAL.fill(pg.Color('brown'))
IMAGE_HOVER = pg.Surface((100, 32))
IMAGE_HOVER.fill(pg.Color('brown'))
IMAGE_DOWN = pg.Surface((100, 32))
IMAGE_DOWN.fill(pg.Color('black'))

def displayimage(Imagename,x,y):
    screen.blit(Imagename,(x,y))

class Button(pg.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,
                 font=FONT, text='', text_color=(0, 0, 0),
                 image_normal=IMAGE_NORMAL, image_hover=IMAGE_HOVER,
                 image_down=IMAGE_DOWN):

        super().__init__()

        self.image_normal = pg.transform.scale(image_normal, (width, height))
        self.image_hover = pg.transform.scale(image_hover, (width, height))
        self.image_down = pg.transform.scale(image_down, (width, height))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))

        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)

        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
        elif event.type == pg.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pg.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal

class Screen:
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            for button in self.all_sprites:
                button.handle_event(event)

    def run_logic(self):
        self.all_sprites.update(self.dt)

class StartScreen(Screen):

    def __init__(self, screen):
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = screen

        self.all_sprites = pg.sprite.Group()

        self.start_button = Button(
            150, 550, 200, 65, self.start_game,
            FONT, 'Game Start', (255, 255, 255),
            IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN)

        self.quit_button = Button(
            850, 550, 200, 65, self.quit_game,
            FONT, 'Quit', (255, 255, 255))

        self.how_to_play_button = Button(
            500, 550, 200, 65, self.how_to_play,
            FONT, 'How To Play', (255, 255, 255))

        self.all_sprites.add(self.start_button, self.quit_button,self.how_to_play_button)

    def quit_game(self):
        self.done = True
        global F
        F = 0

    def start_game(self):
        global F
        F = 3

    def how_to_play(self):
        global F
        F = 2

    def run(self):
        while not self.done and F == 1:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def draw(self):
        displayimage(Background,0,0)
        displayimage(Title,150,150)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

class HowToPlayScreen(Screen):
    def __init__(self, screen):
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = screen
        self.all_sprites = pg.sprite.Group()

        self.back_button = Button(
        500, 700, 200, 65, self.back,
        FONT, 'Back', (255, 255, 255),
        IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN)

        self.all_sprites.add(self.back_button)

    def back(self):
        global F
        F = 1

    def run(self):
        while not self.done and F == 2:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def draw(self):
        displayimage(HowToPlayImg,0,0)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

class GameplayScreen(Screen):
    def __init__(self, screen):
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = screen
        self.all_sprites = pg.sprite.Group()

        self.minigame_button = Button(
        50, 700, 200, 65, self.minigame_start,
        FONT, 'Minigame', (255, 255, 255),
        IMAGE_NORMAL, IMAGE_HOVER, IMAGE_DOWN)

        self.Boss_button = Button(
        950, 700, 200, 65, self.Boss_start,
        FONT, 'Boss Game', (255, 255, 255))

        self.all_sprites.add(self.Boss_button,self.minigame_button)

    def minigame_start(self):
        global ticket,best_character,dataformini
        playerdata['Name']=dataformini[best_character][1]
        playerdata['rank']=dataformini[best_character][2]
        playerdata['count']=dataformini[best_character][3]
        playerimage1=dataformini[best_character][0]
        V = minigame.main(playerdata,playerimage1)
        if V == 1:
            ticket += 10*(best_character+1)
        elif V == 0:
            pass
        print(ticket)
    def Boss_start(self):
        global ticket,best_character,dataforboss
        playerdata['Name'] = dataforboss[best_character][1]
        playerdata['rank'] = dataforboss[best_character][2]
        playerdata['count'] = dataforboss[best_character][3]
        playerimage2 = dataforboss[best_character][0]
        boss.setting(playerdata,playerimage2)
        V = boss.main()
        if V == 1:
            ticket += 10*(best_character+1)
        elif V == 0:
            pass
        print(ticket)

    def run(self):
        global counter,cnt_checked_character,fontnormal,tickettext,ticket
        while not self.done and F == 3:
            self.dt = self.clock.tick(30) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()
            counter += 1
            cnt_checked_character = 0
            for i in range(4):
                for j in range(4):
                    if character_checked[i][j] == 1:
                        cnt_checked_character = cnt_checked_character + 1
            flag = 1
            if counter % 10 == 0:
                global best_character
                for i in range(4):
                    for j in range(4):
                        if best_character < is_image[i][j]:
                            best_character = is_image[i][j]
                for i in range(4):
                    for j in range(4):
                        if is_image[i][j] == -1 and flag == 1:
                            screen.blit(maze_runner_character_image[0], (j * 100+400, i * 100+200))
                            is_image[i][j] = 0
                            pg.display.update()
                            flag = 0
                    if flag == 0:
                        break

    def handle_events(self):
        global cnt_checked_character,ticket
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    for i in range(4):
                        for j in range(4):
                            if is_image[i][j] != -1 and mouse_x > range_check[j]+400 and mouse_x < range_check[j + 1]+400 and mouse_y > range_check[i]+200 and mouse_y < range_check[i + 1]+200 and character_checked[i][j] == 0 and is_image[i][j] < 9 and cnt_checked_character < 2:
                                screen.blit(check, (range_check[j]+400, range_check[i]+200))
                                pg.display.update()
                                character_checked[i][j] = 1
                                cnt_checked_character = cnt_checked_character + 1
                                ticket = update_character(i,j,ticket)

                            elif is_image[i][j] != -1 and mouse_x > range_check[j]+400 and mouse_x < range_check[j + 1]+400 and mouse_y > range_check[i]+200 and mouse_y < range_check[i + 1]+200 and character_checked[i][j] == 1:
                                character_checked[i][j] = 0
                                cnt_checked_character = cnt_checked_character - 1
                                screen.blit(maze_runner_character_image[is_image[i][j]],(range_check[j]+400, range_check[i]+200))
                                pg.display.update()
                                # update_character(i,j)
            for button in self.all_sprites:
                button.handle_event(event)
    def draw(self):
        global fontnormal,best_character,dataforboss
        displayimage(GamePlayImg, 0, 0)
        global tickettext
        for i in range(4):
            for j in range(4):
                if is_image[i][j] != -1:
                    screen.blit(maze_runner_character_image[is_image[i][j]],(range_check[j]+400, range_check[i]+200))
                if character_checked[i][j] == 1:
                    screen.blit(check,(range_check[j]+400, range_check[i]+200))
        tickettext = fontnormal.render("%s" % (ticket), True, (0, 0, 0))
        besttext = fontnormal.render("%s" % (dataforboss[best_character][1]), True, (0, 0, 0))
        screen.blit(tickettext, (80, 250))
        best=pygame.transform.scale(maze_runner_character_image[best_character],(200,200))
        screen.blit(best,(900,300))
        screen.blit(besttext,(900,220))
        self.all_sprites.draw(self.screen)
        pg.display.flip()

if __name__ == '__main__':
    while F != 0:
        if F == 1:
            StartScreen(screen).run()
        elif F == 2:
            HowToPlayScreen(screen).run()
        elif F == 3:
            GameplayScreen(screen).run()
    pg.quit()
