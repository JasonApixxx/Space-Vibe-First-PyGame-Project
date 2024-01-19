import pygame
import random
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image



WIDTH = 900
HEIGHT = 800


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.NOFRAME)
pygame.display.set_caption("Space Vibe")
icon = load_image('Project Images/logo.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
pygame.mixer.music.load('Project Images/Sound_06324.mp3')
burst_sound = pygame.mixer.Sound('Project Images/Sound_02210.mp3')
gameover = pygame.mixer.Sound('Project Images/Sound_19316.mp3')
button_sound = pygame.mixer.Sound('Project Images/Sound_02210 (mp3cut.net).mp3')
score1 = 0
score2 = 0
maximum1 = 0
maximum2 = 0
pygame.time.set_timer(pygame.USEREVENT, 2000)
animation = [pygame.image.load('Project Images/burst.png'),
             pygame.image.load('Project Images/burst2.png'),
             pygame.image.load('Project Images/burst3.png'),
             pygame.image.load('Project Images/burst4.png'),
             pygame.image.load('Project Images/burst5.png'),
             pygame.image.load('Project Images/burst6.png')]
action = ''
sp = []
health = 3
health_image = pygame.image.load("Project Images/spaceship.png")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #инициализируем класс с изображениями
        self.image = ship # присваиваем переменной изображениие корабля
        self.rect = self.image.get_rect() # рисуем невидимый прямоугольник вокруг корабля для получения координат
        self.rect.centerx = WIDTH / 2 # начальная координата по х
        self.rect.bottom = HEIGHT - 10 # по у
        self.speedx = 0 # нулевая скорость

    def update(self): #метод, отвечающий за передвижение корабля
        if health == 2:
            self.image = animation[0]
        if health == 1:
            self.image = animation[2]
        self.speedx = 0
        keystate = pygame.key.get_pressed() # подключаем клавиатуру
        if keystate[pygame.K_LEFT]: # если нажата стрелка влево, корабль будет двигаться влево
            self.speedx = -8
        if keystate[pygame.K_RIGHT]: # если нажата стрелка вправо, корабль будет двигаться вправо
            self.speedx = 8
        self.rect.x += self.speedx # передвигаем корабль в соответствии с нажатием кнопки
        if self.rect.right > WIDTH: # не даём кораблю выйти за экран
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width) #по х метеорит появляется в диапазоне от 0 до ширины экрана - ширина нло
        self.rect.y = random.randrange(-100, -40) # по у метеорит появляется в диапазоне от -100 до -40
        self.speedy = random.randrange(3, 8) # скорость нло по у будет присваиваться в диапазоне от 3 до 8 пикселей
        self.speedx = random.randrange(-3, 3) # по х соответственно от -3 до 3

    def update(self):
        self.rect.x += self.speedx # прибавляем координатам нло их скорость
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: # если нло вышло за пределы экрана, мы его возвращаем на исходную позицию
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)
            self.speedx = random.randrange(-3, 3)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)
            self.speedx = random.randrange(-3, 3)


class Fly_for_player(pygame.sprite.Sprite):
    image = load_image("Project Images/bullet.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Fly_for_player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if True:  # not pygame.sprite.collide_mask(self, ufo):
            self.rect = self.rect.move(0, -8)
            if self.rect.y > HEIGHT:
                self.kill()


class Fly_for_ufo(pygame.sprite.Sprite):
    image = load_image("Project Images/bullet.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Fly_for_player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if True:  # not pygame.sprite.collide_mask(self, ufo):
            self.rect = self.rect.move(0, 9)
            if self.rect.y < -HEIGHT:
                self.kill()


class Button:
    def __init__(self, width, height, color1, color2):
        self.width = width
        self.height = height
        self.color1 = color1
        self.color2 = color2

    def draw(self, x, y, message, action=None, fontsize=30):
        global all_sprites, meteors, ufos, bullets, player, score1, score2, ufo_bullets, player_bullets, sp, text, txt
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            print_text(message=message, x=x + 10, y=y + 10, size=76, color=self.color1)
            if click[0] == 1:
                # pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        text.write(f'{txt[:-1]}:{maximum1}:{maximum2}')
                        exit()
                    if action == gamemenu:
                        score1 = 0
                        score2 = 0
                        all_sprites = pygame.sprite.Group()
                        meteors = pygame.sprite.Group()
                        ufos = pygame.sprite.Group()
                        bullets = pygame.sprite.Group()
                        player = Player()
                        all_sprites.add(player)
                        pygame.time.set_timer(pygame.USEREVENT, 2000)
                    if action == action:
                        if not message == 'continue':
                            score1 = 0
                            score2 = 0
                            all_sprites = pygame.sprite.Group()
                            meteors = pygame.sprite.Group()
                            ufos = pygame.sprite.Group()
                            player_bullets = pygame.sprite.Group()
                            ufo_bullets = pygame.sprite.Group()
                            player = Player()
                            all_sprites.add(player)
                            pygame.time.set_timer(pygame.USEREVENT, 2000)
                    action()

        else:
            print_text(message=message, x=x + 10, y=y + 10, size=76, color=self.color2)

ship = load_image("Project Images/spaceship.png")
meteor_ = load_image("Project Images/meteor.png")
background = load_image('Project Images/background.jpg')
ufo = load_image('Project Images/ufo (2).png')
bullet = load_image('Project Images/bullet.png')
background_rect = background.get_rect()


all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
ufos = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
ufo_bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True


bg_y = 0
meteor = ''
collide = ''


def exit():         #самая бесполезная функция в мире
    pygame.quit()
    quit()


def print_text(message, x, y, color=(255, 255, 255), type='Project Images/SpaceMission.otf', size=30):
    type = pygame.font.Font(type, size)
    text = type.render(message, True, color)
    screen.blit(text, (x, y))


def get_text():
    global need_input, txt, input_tick, text, score, maximum1, maximum2, sp
    input_rect = pygame.Rect(260, 300, 370, 70)
    pygame.draw.rect(screen, (255, 255, 255), input_rect, 10)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    if input_rect.collidepoint(mouse[0], mouse[1]) and click[0]:
        need_input = True
        txt = ''
    for even in pygame.event.get():
        if need_input and even.type == pygame.KEYDOWN:
            txt = txt.replace('|', '')
            input_tick = 30
            if even.key == pygame.K_RETURN:
                need_input = False
                txt += ' '
            elif even.key == pygame.K_BACKSPACE:
                txt = txt[:-1]
            else:
                if len(txt) < 10:
                    txt += even.unicode
            txt += '|'
    if need_input:
        input_tick -= 1
        if input_tick == 0:
            txt = txt[:txt.find('|')]

        if input_tick == -30:
            txt += '|'
            input_tick = 30
    else:
        txt = txt.replace('|', '')
    if len(txt):
        print_text(txt, 270, 303, size=60)

for_continue = ''
need_input = False
txt = ''
input_tick = 30
text = open('txt.txt', 'w', encoding='utf8')


def gamemenu():
    global running, bg_y, hero_image, need_input
    # pygame.mixer.music.play(-1)
    start_button = Button(200, 70, 'yellow', 'white')
    quit_button = Button(200, 70, 'yellow', 'white')
    runnin = True
    need_input = False
    while runnin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                runnin = False
        screen.blit(background, (0, bg_y - 800))
        screen.blit(background, (0, bg_y))
        bg_y += 2
        if bg_y == 800:
            bg_y = 0

        print_text('Space vibe', 200, 150, size=100)
        start_button.draw(100, 500, 'play', level, 50)
        quit_button.draw(550, 500, 'quit', quit, 50)
        print_text('nickname:', 10, 317, size=50)
        get_text()
        pygame.display.update()
        clock.tick(60)



def show_health():
    global health
    show = 0
    x = 20
    while show != health:
        screen.blit(health_image, (x, 20))
        x += 65
        show += 1
def check_health():
    global health
    health -= 1
    if health == 0:
        return False
    return True

def start_game(): #метеориты
    global running, bg_y, score1,  all_sprites, meteors, player, action, for_continue, maximum1, text, health
    action = start_game
    health = 3
    for_continue = start_game
    while running:
        screen.blit(background, (0, bg_y - 800))
        screen.blit(background, (0, bg_y))
        print_text("Score: " + str(score1), 740, 30)
        clock.tick(60)
        keys = pygame.key.get_pressed()
        game_over_ = False
        bg_y += 2
        if bg_y == 800:

            bg_y = 0
        all_sprites.draw(screen)
        for i in meteors:
            if i.rect.colliderect(player.rect):
                if score1 > maximum1:
                    maximum1 = score1
                    sp.append(str(maximum1))
                if not check_health():
                    for j in range(6):
                        screen.blit(animation[j], (player.rect.x, player.rect.y))
                        pygame.time.set_timer(pygame.USEREVENT, 0)
                        game_over_ = True
                else:
                    i.kill()
                #     all_sprites = pygame.sprite.Group()
                #     meteors = pygame.sprite.Group()
                #     player = Player()
                #     all_sprites.add(player)
                #     pygame.time.set_timer(pygame.USEREVENT, 2000)
                #     if pygame.USEREVENT:
                #         score1 += 1
                #         for i in range(2):
                #             meteor = Meteor()
                #             all_sprites.add(meteor)
                #             meteors.add(meteor)
                # for event in pygame.event.get():
                #     keys = pygame.key.get_pressed()
                #     if event.type == pygame.QUIT:
                #         running = False
                #         exit()
                #     if event.type == pygame.USEREVENT:
                #         score1 += 1
                #         for i in range(2):
                #             meteor = Meteor()
                #             all_sprites.add(meteor)
                #             meteors.add(meteor)
        show_health()

        if game_over_:
            print_text(f'your score: {score1}, best:{maximum1}', 50, 300, size=70)
            game_over()
            score1 = 0
            game_over_ = False
            health = 3
            all_sprites = pygame.sprite.Group()
            meteors = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            pygame.time.set_timer(pygame.USEREVENT, 2000)
            if pygame.USEREVENT:
                score1 += 1
                for i in range(2):
                    meteor = Meteor()
                    all_sprites.add(meteor)
                    meteors.add(meteor)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.USEREVENT:
                score1 += 1
                for i in range(2):
                    meteor = Meteor()
                    all_sprites.add(meteor)
                    meteors.add(meteor)

            if keys[pygame.K_ESCAPE]:
                pause()
        all_sprites.update()
        pygame.display.flip()


def uFo(): # НЛО
    global running, bg_y, score2, all_sprites, ufos, player, action, for_continue, ufo_bullets, player_bullets, maximum2
    action = uFo
    for_continue = uFo
    while running:
        screen.blit(background, (0, bg_y - 800))
        screen.blit(background, (0, bg_y))
        print_text("Score: " + str(score2), 740, 30)
        clock.tick(60)
        keys = pygame.key.get_pressed()
        game_over_ = False
        bg_y += 2
        if bg_y == 800:
            bg_y = 0
        all_sprites.draw(screen)
        for a in ufo_bullets:
            if a.rect.colliderect(player.rect):
                if score2 > maximum2:
                    maximum2 = score2
                    sp.append(str(maximum2))
                # pygame.mixer.Sound.play(burst_sound)
                for j in range(6):
                    screen.blit(animation[j], (player.rect.x, player.rect.y))
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    game_over_ = True

        for j in ufos:
            for k in ufo_bullets:
                for i in player_bullets:
                    if j.rect.colliderect(player.rect):
                        for x in range(6):
                            screen.blit(animation[x], (player.rect.x, player.rect.y))
                            pygame.time.set_timer(pygame.USEREVENT, 0)
                            game_over_ = True
                    if i.rect.colliderect(j.rect):
                        j.kill()
                        i.kill()
                        k.kill()
        if game_over_:
            print_text(f'your score: {score2}, best:{maximum2}', 50, 300, size=70)
            game_over()

            score2 = 0
            all_sprites = pygame.sprite.Group()
            meteors = pygame.sprite.Group()
            ufos = pygame.sprite.Group()
            player_bullets = pygame.sprite.Group()
            ufo_bullets = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            pygame.time.set_timer(pygame.USEREVENT, 2000)
            if pygame.USEREVENT:
                score2 += 1
                ufol = Ufo()
                all_sprites.add(ufol)
                ufos.add(ufol)
                c = Fly_for_ufo((ufol.rect.x, ufol.rect.y))
                all_sprites.add(c)
                ufo_bullets.add(c)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == pygame.USEREVENT:
                score2 += 1
                for i in range(2):
                    ufol = Ufo()
                    all_sprites.add(ufol)
                    ufos.add(ufol)
                for i in ufos:
                    c = Fly_for_ufo((i.rect.x, i.rect.y))
                    all_sprites.add(c)
                    ufo_bullets.add(c)
            if keys[pygame.K_ESCAPE]:
                pause()
            if keys[pygame.K_SPACE]:
                b = Fly_for_player((player.rect.x, player.rect.y))
                all_sprites.add(b)
                player_bullets.add(b)

        all_sprites.update()

        pygame.display.flip()


def level(): #выбор уровня
    # pygame.mixer.music.play(-1)
    global bg_y
    menu = load_image('Project Images/gamemenu.jpg')
    one = Button(200, 70, 'yellow', 'white')
    two = Button(200, 70, 'yellow', 'white')
    runnin = True

    while runnin:
        screen.blit(background, (0, bg_y - 800))
        screen.blit(background, (0, bg_y))
        bg_y += 2
        if bg_y == 800:
            bg_y = 0
        keys = pygame.key.get_pressed()
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                exit()
            if keys[pygame.K_ESCAPE]:
                gamemenu()
        print_text('Choose level', 200, 150, size=100)
        one.draw(100, 500, '1', start_game, 50)
        two.draw(550, 500, '2', uFo, 50)
        print_text(f'Best: {maximum1}', 50, 650, size=70)
        print_text(f'Best: {maximum2}', 550, 650, size=70)
        pygame.display.update()
        clock.tick(60)


def pause():  # пауза

    paused_ = True
    continu = Button(200, 70, 'yellow', 'white')
    quit = Button(200, 70, 'yellow', 'white')

    while paused_:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        print_text('Paused. continue?', 200, 100)
        pygame.draw.rect(screen, (255, 0, 0), (190, 80, 510, 70), 5)
        continu.draw(100, 500, 'continue', for_continue, 50)
        quit.draw(500, 500, 'main menu', gamemenu, 50)
        keys = pygame.key.get_pressed()
        pygame.display.update()
        clock.tick(15)


def game_over(): # гейм овер

    quit = Button(200, 70, 'yellow', 'white')
    restart = Button(200, 70, 'yellow', 'white')
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        print_text(f'you lose. Restart?', 200, 100)
        pygame.draw.rect(screen, (255, 0, 0), (190, 80, 510, 70), 5)
        restart.draw(100, 500, 'restart', action, 50)
        quit.draw(500, 500, 'main menu', gamemenu, 50)
        pygame.display.update()
        clock.tick(15)


gamemenu()
exit()

