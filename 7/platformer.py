# -*- coding: utf-8 -*-
# Karol "Kenji Takahashi" Wozniak (C) 2012
# GFX by Marc Russell (http://www.spicypixel.net, license included)

import pygame
from pygame.locals import *
from sys import exit


def _makeani(path):
    image = pygame.image.load(path)
    l = list()
    for  i in range(8):
        img = pygame.Surface((32, 32))
        img.blit(image, (0, 0), (i * 32, 0, 32, 32))
        img.set_colorkey((255, 0, 255))
        l.append(img)
    return l


def _makebullet(path=""):
    image = pygame.image.load('gfx/bullet{0}.png'.format(path))
    l = list()
    for i in range(4):
        img = pygame.Surface((16, 16))
        img.blit(image, (0, 0), (i * 16, 0, 16, 16))
        img.set_colorkey((255, 0, 255))
        l.append(img)
    return l


class Hero(pygame.sprite.Sprite):
    _anileft = _makeani('gfx/gripe.run_left.png')
    _aniright = _makeani('gfx/gripe.run_right.png')

    def __init__(self, position):
        super(Hero, self).__init__()
        self.x, self.y = position
        self.ground = self.y
        self.prev = position
        self.vx = self.vy = 0
        self.ani = 0
        self.image = Hero._aniright[self.ani]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.collided = False
        self.wait = 0

    def update(self, end):
        self.prev = self.x, self.y
        self.x += self.vx
        if self.y > self.ground - 50 or self.vy > 0:  # we can hang, no good
            self.y += self.vy
        if self.y < self.ground:
            self.vy += 0.4
        if self.x < 0:
            self.x = 0
        if self.x > 608:
            self.x = 608
        self.rect.left = self.x
        self.rect.top = self.y
        if self.x > 340 and not end:
            self.x = 340
            self.rect.left = self.x
        if self.wait:
            self.wait -= 1

    def ride(self, key):
        self.ani += 1
        self.ani %= 8
        self.vx = 0
        if key[K_UP] and self.y > self.ground - 50:
            self.vy -= 1
        if key[K_DOWN]:
            self.shot()
        if key[K_LEFT]:
            self.vx = -3
            self.image = Hero._anileft[self.ani]
        elif key[K_RIGHT]:
            self.vx = 3
            self.image = Hero._aniright[self.ani]
            return self.x == 340

    def collision(self, rect):
        if rect.top + 2 <= self.rect.bottom:
            self.x, self.y = self.prev
            self.rect.left = self.x
            self.y = self.ground
            self.rect.top = self.ground
            self.vy = 0
            self.collided = True
        else:
            self.collided = False

    def shouldNotMove(self):
        return self.x == 340 and self.collided

    def shot(self, bullets):
        if not self.wait:
            bullets.add(Bullet(3, (self.rect.right, self.rect.centery - 5)))
            self.wait = 45

    def die(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Bullet(pygame.sprite.Sprite):
    _ally = _makebullet()
    _foe = _makebullet("green")

    def __init__(self, type, position):
        super(Bullet, self).__init__()
        self.x, self.y = position
        self.ground = self.x
        self.ani = 0
        self.image = type == 3 and Bullet._ally[0] or Bullet._foe[0]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.vx = type

    def update(self):
        if self.x > self.ground + 120:
            self.kill()
        else:
            self.ani += 1
            self.ani %= 4
            self.image = self.vx == 3\
            and Bullet._ally[self.ani] or Bullet._foe[self.ani]
            self.x += self.vx
            self.rect.left = self.x


class Coin(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Coin, self).__init__()


class Platform(pygame.sprite.Sprite):
    _image = pygame.image.load('gfx/01/platform.png')
    _image.set_colorkey((255, 0, 255))

    def __init__(self, position, offset):
        super(Platform, self).__init__()
        self.x, self.y = position
        self.ground = self.x
        self.image = Platform._image
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.offset = offset
        self.ooffset = offset

    def update(self, yes):
        if self.x + self.rect.width < 0:
            self.kill()
        else:
            if not yes:
                self.x -= 3
                self.ground -= 3
            if self.offset:
                self.x += 3
                self.offset -= 3
            else:
                self.x -= 3
            if self.x == self.ground:
                self.offset = self.ooffset
            self.rect.left = self.x


class Piece(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super(Piece, self).__init__()
        self.x, self.y = position
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    def update(self):
        if self.x + self.rect.width < 0:
            self.kill()
        else:
            self.x -= 3
            self.rect.left = self.x


class Game(pygame.sprite.Sprite):
    _levels = [None,  # magic bit
        (  # 1st level
            417,  # player starting position
            448,  # level length
            [
                [(14, 448, False), (8, 400, False)],
                [
                    (14, 464, False),
                    (8, 416, True),
                    (8, 432, True),
                    (8, 448, True),
                    (8, 464, True)
                ]
            ],  # ground spec
            [
                [(720, 400, 84)]
            ],  # platforms spec
            [
            ]  # enemies spec
        ),
        (  # 2nd level
        )
    ]

    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load('gfx/01/b.png').convert()
        self.rect = self.image.get_rect()
        self.x = 0
        self.pieces = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.level = 1
        self.ppos, self.width, ground, platforms, enemies\
        = Game._levels[self.level]
        for i in range(len(ground)):
            piece = pygame.image.load('gfx/01/p{0}.png'.format(i)).convert()
            piece.set_colorkey((255, 0, 255))
            curpos = 0
            for num, height, boo in ground[i]:
                for j in range(num):
                    self.pieces.add(Piece(piece, (32 * j + curpos, height)))
                if not boo:
                    curpos += num * 32
        for x, y, o in platforms[self.level - 1]:
            self.platforms.add(Platform((x, y), o))
        self.hero = Hero((15, self.ppos))

    def update(self, moving):
        if not self.hero.shouldNotMove() and moving:
            self.x += 3
            self.pieces.update()
            self.platforms.update(False)
        else:
            self.platforms.update(True)

    def draw(self):
        x = self.x % 640
        self.screen.blit(self.image, (0, 0), (x, 0, 640 - x, 480))
        if x:
            self.screen.blit(self.image, (640 - x, 0), (0, 0, 640, 480))
        self.pieces.draw(self.screen)

    def run(self):
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[K_LCTRL]:
                self.hero.shot(self.bullets)
            moving = self.hero.ride(keys)
            self.hero.update(self.x >= self.width)
            die = True
            for p in self.pieces:
                if pygame.sprite.collide_rect(p, self.hero):
                    self.hero.collision(p.rect)
                    die = False
            if die and self.hero.die():
                pass
            self.update(moving)
            self.bullets.update()
            self.draw()
            self.platforms.draw(self.screen)
            self.hero.draw(self.screen)
            self.bullets.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
