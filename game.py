from typing import Any
from pygame import *
from random import randint

font.init()
font2 = font.Font(None, 33)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w=65, h=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Ball(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
lost = 0

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed

    def fire(self):
        ball = Ball("ball.png", self.rect.centerx, self.rect.top, -15, 20, 20)
        balls.add(ball)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


monsters = sprite.Group()
balls = sprite.Group()
font1 = font.Font(None, 36)
font2 = font.Font(None, 80)
win = font2.render("YOU SCORED GOAL", True, (255, 255, 255))
lose = font2.render("YOU MISS", True, (255, 255, 255))

score = 0
lost = 0
for i in range(1, 6):
    monster = Enemy("3F.webp", randint(80, win_width - 80), -40, randint(1, 5))
    monsters.add(monster)

txt_lose = font2.render("Промазав: " + str(lost), 1, (255, 255, 255))
window = display.set_mode((win_width, win_height))
display.set_caption("Шутка")
background = transform.scale(image.load("бєкграунд.jpg"), (win_width, win_height))

player = Player("Шева.jpg", 5, win_height - 80, 5)
monster = Enemy("3F.webp", 350, win_height - 400, 2)

score = 0
lost = 0
goal = 5
max_lost = 7
clock = time.Clock()
FPS = 60
game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    if not finish:
        window.blit(background, (0, 0))
        text = font1.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        txt_lose = font1.render("Промазав: " + str(lost), 1, (255, 255, 255))
        window.blit(txt_lose, (10, 50))

        player.update()
        monsters.update()
        monsters.draw(window)
        balls.update()
        balls.draw(window)

        if sprite.groupcollide(monsters, balls, True, True):
            score += 1
            monster = Enemy("3F.webp", randint(80, win_width - 80), -40, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (100, 200))

        player.reset()

    display.update()
    clock.tick(FPS)