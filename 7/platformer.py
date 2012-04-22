# -*- coding: utf-8 -*-

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


class Hero(pygame.sprite.Sprite):
    _anileft = _makeani('gfx/gripe.run_left.png')
    _aniright = _makeani('gfx/gripe.run_right.png')

    def __init__(self, position):
        super(Hero, self).__init__()
        self.x, self.y = position
        self.prev = position
        self.vx = self.vy = 0
        self.ani = 0
        self.image = Hero._aniright[self.ani]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.collided = False

    def update(self, end):
        self.prev = self.x, self.y
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.x = 0
        if self.x > 608:
            self.x = 608
        self.rect.left = self.x
        self.rect.top = self.y
        if self.x > 340 and not end:
            self.x = 340
            self.rect.left = self.x

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))

    def ride(self, key):
        self.ani += 1
        self.ani %= 8
        self.vx = 0
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
            self.vy = 0
            self.collided = True
        else:
            self.collided = False

    def shouldNotMove(self):
        return self.x == 340 and self.collided

    def jump(self):
        pass

    def shot(self):
        pass

    def die(self):
        pass


class Platform(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Platform, self).__init__()


class Piece(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super(Piece, self).__init__()
        self.x, self.y = position
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    def update(self, yes):
        if self.x + self.rect.width < 0:
            self.kill()
        else:
            if yes:
                self.x += 3
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
        self.level = 1
        self.ppos, self.width, ground, platforms, enemies\
        = Game._levels[self.level]
        for i in range(len(Game._levels) - 1):
            piece = pygame.image.load('gfx/01/p{0}.png'.format(i)).convert()
            piece.set_colorkey((255, 0, 255))
            curpos = 0
            for num, height, boo in ground[i]:
                for j in range(num):
                    self.pieces.add(Piece(piece, (32 * j + curpos, height)))
                if not boo:
                    curpos += num * 32
        self.hero = Hero((15, self.ppos))

    def update(self, moving):
        if not self.hero.shouldNotMove() and moving:
            self.x += 3
            self.pieces.update(False)

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
                if event.type == KEYDOWN and event.key == K_UP:
                    self.hero.jump()
            keys = pygame.key.get_pressed()
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
            self.draw()
            self.hero.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
