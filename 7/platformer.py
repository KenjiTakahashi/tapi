# -*- coding: utf-8 -*-
# Karol "Kenji Takahashi" Wozniak (C) 2012
# GFX by Marc Russell (http://www.spicypixel.net, license included)

import pygame
from pygame.locals import *
from sys import exit
from random import randint


def _makeani(path, n):
    image = pygame.image.load(path)
    l = list()
    for  i in range(n):
        img = pygame.Surface((32, 32))
        img.blit(image, (0, 0), (i * 32, 0, 32, 32))
        img.set_colorkey((255, 0, 255))
        l.append(img)
    return l


def _makethumb():
    image = pygame.image.load('gfx/gripe.run_right.png')
    img = pygame.Surface((32, 32))
    img.blit(image, (0, 0), (0, 0, 32, 32))
    img.set_colorkey((255, 0, 255))
    return pygame.transform.scale(img, (16, 16))


def _makebullet(path=""):
    image = pygame.image.load('gfx/bullet{0}.png'.format(path))
    l = list()
    for i in range(4):
        img = pygame.Surface((16, 16))
        img.blit(image, (0, 0), (i * 16, 0, 16, 16))
        img.set_colorkey((255, 0, 255))
        l.append(img)
    return l


def _makeexit():
    image = pygame.image.load('gfx/exit.png')
    l = list()
    for i in range(8):
        img = pygame.Surface((64, 64))
        img.blit(image, (0, 0), (i * 64, 0, 64, 64))
        img.set_colorkey((255, 0, 255))
        l.append(img)
    return l


def _makecoin():
    image = pygame.image.load('gfx/coin.png')
    l = list()
    for i in range(8):
        img = pygame.Surface((16, 16))
        img.blit(image, (0, 0), (i * 16, 0, 16, 16))
        img.set_colorkey((255, 0, 255))
        l.append(img)
    return l


class Hero(pygame.sprite.Sprite):
    _ani = (
        _makeani('gfx/gripe.run_right.png', 8),
        _makeani('gfx/gripe.run_left.png', 8)
    )
    _jump = (
        pygame.image.load('gfx/gripe.jump_right.png'),
        pygame.image.load('gfx/gripe.jump_left.png')
    )
    _jump[0].set_colorkey((255, 0, 255))
    _jump[1].set_colorkey((255, 0, 255))

    def __init__(self, position):
        super(Hero, self).__init__()
        self.x, self.y = position
        self.ground = self.y
        self.prev = position
        self.vx = self.vy = 0
        self.ani = 0
        self.direction = 0
        self.image = Hero._ani[self.direction][self.ani]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.collided = False
        self.wait = 0
        self.jump = False
        self.offset = 100
        self.flying = 15
        self.ooffset = self.offset
        self.hang = 0
        self.dying = False

    def update(self, end):
        self.prev = self.x, self.y
        self.x += self.vx
        if self.jump:
            if self.offset:
                self.y -= self.flying
                self.offset -= self.flying
                self.flying -= 1
                if not self.offset:
                    self.hang = 3
            elif not self.hang:
                self.flying += 1
                self.y += self.flying
            else:
                self.hang -= 1
            self.image = Hero._jump[self.direction]
        else:
            self.image = Hero._ani[self.direction][self.ani]
        if self.dying:
            self.y += 7
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

    def _jumpoff(self):
        self.ground = self.y
        self.offset = self.ooffset
        self.jump = False
        self.flying = 15

    def _animate(self):
        self.ani += 1
        self.ani %= 8

    def ride(self, key):
        self.vx = 0
        if key[K_UP] and self.ground == self.y:
            self.jump = True
        if key[K_LEFT]:
            self._animate()
            self.vx = -3
            self.direction = 1
        elif key[K_RIGHT]:
            self._animate()
            self.vx = 3
            self.direction = 0
            return self.x == 340

    def collision(self, rect):
        if not rect.colliderect((self.prev, (32, 32))):
            self.y = rect.top - 31
            self.rect.top = self.y
            self.prev = (self.prev[0], self.y)
            self.dying = False
            self._jumpoff()
        elif not self.jump and rect.top + 2 <= self.rect.bottom:
            self.collided = True
            return True

    def shouldNotMove(self):
        r = self.x == 340 and self.collided
        self.collided = False
        return r

    def shot(self, bullets):
        if not self.wait:
            if self.direction:
                vx = -5
                x = self.rect.left - 16
            else:
                vx = 5
                x = self.rect.right
            bullets.add(Bullet(1, vx, (x, self.rect.centery - 5)))
            self.wait = 35

    def die(self):
        if not self.jump:
            self.dying = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class NormalFoe(pygame.sprite.Sprite):
    _left = _makeani('gfx/wheelie_left.png', 4)
    _right = _makeani('gfx/wheelie_right.png', 4)
    _dieleft = pygame.image.load('gfx/wheelie_die_left.png')
    _dieleft.set_colorkey((255, 0, 255))
    _dieright = pygame.image.load('gfx/wheelie_die_right.png')
    _dieright.set_colorkey((255, 0, 255))

    def __init__(self, position, offset):
        super(NormalFoe, self).__init__()
        self.x, self.y = position
        self.ground = self.x
        self.ani = 0
        self.image = NormalFoe._left[self.ani]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.offset = offset
        self.ooffset = offset
        self.died = 0

    def update(self, yes):
        if self.died:
            self.died -= 1
        if self.x + self.rect.width < 0 or self.died == 1:
            self.kill()
        elif not self.died:
            self.ani += 1
            self.ani %= 4
            if not yes:
                self.x -= 3
                self.ground -= 3
            if self.offset:
                self.x += 3
                self.offset -= 3
                self.image = NormalFoe._right[self.ani]
            else:
                self.x -= 3
                self.image = NormalFoe._left[self.ani]
            if self.x == self.ground:
                self.offset = self.ooffset
            self.rect.left = self.x

    def die(self):
        if self.offset:
            self.image = NormalFoe._dieright
        else:
            self.image = NormalFoe._dieleft
        self.died = 10


class ShootingFoe(pygame.sprite.Sprite):
    _left = _makeani('gfx/grog.left.png', 8)
    _right = _makeani('gfx/grog.right.png', 8)
    _dieleft = pygame.image.load('gfx/grog.left.die.png')
    _dieleft.set_colorkey((255, 0, 255))
    _dieright = pygame.image.load('gfx/grog.right.die.png')
    _dieright.set_colorkey((255, 0, 255))

    def __init__(self, position, offset, bullets):
        super(ShootingFoe, self).__init__()
        self.x, self.y = position
        self.ground = self.x
        self.ani = 0
        self.image = ShootingFoe._right[self.ani]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.offset = offset
        self.ooffset = offset
        self.bullets = bullets
        self.wait = 0
        self.died = 0

    def update(self, yes):
        if self.died:
            self.died -= 1
        if self.x + self.rect.width < 0 or self.died == 1:
            self.kill()
        elif not self.died:
            self.ani += 1
            self.ani %= 8
            if not yes:
                self.x -= 3
                self.ground -= 3
            if self.offset:
                self.x += 3
                self.offset -= 3
                self.image = ShootingFoe._right[self.ani]
            else:
                self.x -= 3
                self.image = ShootingFoe._left[self.ani]
            if self.x == self.ground:
                self.offset = self.ooffset
            self.rect.left = self.x
            if not self.wait and self.x < 640:
                self.fire()
                self.wait = 40
            elif self.wait:
                self.wait -= 1

    def fire(self):
        if self.offset:
            vx = 5
            x = self.rect.right
        else:
            vx = -5
            x = self.rect.left - 16
        self.bullets.add((Bullet(0, vx, (x, self.rect.centery - 5))))

    def die(self):
        if self.offset:
            self.image = ShootingFoe._dieright
        else:
            self.image = ShootingFoe._dieleft
        self.died = 10


class Bullet(pygame.sprite.Sprite):
    _ally = _makebullet()
    _foe = _makebullet("green")

    def __init__(self, type, vx, position):
        super(Bullet, self).__init__()
        self.x, self.y = position
        self.ground = self.x
        self.ani = 0
        self.type = type
        self.image = type == 1 and Bullet._ally[0] or Bullet._foe[0]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.vx = vx

    def update(self, yes):
        if self.x > self.ground + 120 or self.x < self.ground - 120:
            self.kill()
        else:
            self.ani += 1
            self.ani %= 4
            self.image = self.type == 1\
            and Bullet._ally[self.ani] or Bullet._foe[self.ani]
            if not yes:
                self.x -= 3
            self.x += self.vx
            self.rect.left = self.x


class Coin(pygame.sprite.Sprite):
    _images = _makecoin()

    def __init__(self, position):
        super(Coin, self).__init__()
        self.x, self.y = position
        self.ani = 0
        self.image = Coin._images[self.ani]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    def update(self, yes):
        if self.x + self.rect.width < 0:
            self.kill()
        else:
            if not yes:
                self.x -= 3
                self.rect.left = self.x
            self.ani += 1
            self.ani %= 8
            self.image = Coin._images[self.ani]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


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


class Exit(pygame.sprite.Sprite):
    _images = _makeexit()

    def __init__(self, position):
        super(Exit, self).__init__()
        self.x, self.y = position
        self.ani = 0
        self.image = Exit._images[self.ani]
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    def update(self, yes):
        self.ani += 1
        self.ani %= 8
        self.image = Exit._images[self.ani]
        if not yes:
            self.x -= 3
            self.rect.left = self.x

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Game(pygame.sprite.Sprite):
    _levels = [None,  # magic bit
        (  # 1st level
            417,  # player starting position
            448,  # level length
            [
                [(14, 448, 0), (8, 400, 448), (6, 416, 904)],
                [
                    (14, 464, 0),
                    (8, 416, 448),
                    (8, 432, 448),
                    (8, 448, 448),
                    (8, 464, 448),
                    (6, 432, 904),
                    (6, 448, 904),
                    (6, 464, 904)
                ]
            ],  # ground spec
            [
                [(720, 400, 84)]
            ],  # platforms spec
            [
                [(440, 320), (460, 320), (480, 320), (500, 320)]
            ],  # coins spec
            [
                [(0, 450, 369, 72), (1, 910, 385, 84)]
            ],  # foes spec
            (1030, 352)  # exit
        ),
        (  # 2nd level
        )
    ]
    _thumb = _makethumb()

    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(None, 20)
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load('gfx/01/b.png').convert()
        self.rect = self.image.get_rect()
        self.x = 0
        self.points = 0
        self.lifes = 3
        self.coin = Coin((3, 5))
        self.pieces = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.foes = pygame.sprite.Group()
        self.level = 1
        self.ppos, self.width, ground, platforms, coins, foes, exit_\
        = Game._levels[self.level]
        for i in range(len(ground)):
            piece = pygame.image.load('gfx/01/p{0}.png'.format(i)).convert()
            piece.set_colorkey((255, 0, 255))
            for num, height, start in ground[i]:
                for j in range(num):
                    self.pieces.add(Piece(piece, (32 * j + start, height)))
        for x, y, o in platforms[self.level - 1]:
            self.platforms.add(Platform((x, y), o))
        for x, y in coins[self.level - 1]:
            self.coins.add(Coin((x, y)))
        for t, x, y, o in foes[self.level - 1]:
            if not t:
                self.foes.add(NormalFoe((x, y), o))
            else:
                self.foes.add(ShootingFoe((x, y), o, self.bullets))
        self.exit = Exit(exit_)
        self.hero = Hero((15, self.ppos))

    def update(self, moving):
        if not self.hero.shouldNotMove() and moving:
            self.x += 3
            self.pieces.update()
            self.platforms.update(False)
            self.coins.update(False)
            self.foes.update(False)
            self.bullets.update(False)
            self.exit.update(False)
        else:
            self.platforms.update(True)
            self.coins.update(True)
            self.foes.update(True)
            self.bullets.update(True)
            self.exit.update(True)

    def draw(self):
        x = self.x % 640
        self.screen.blit(self.image, (0, 0), (x, 0, 640 - x, 480))
        if x:
            self.screen.blit(self.image, (640 - x, 0), (0, 0, 640, 480))
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 640, 24))
        self.screen.blit(self.font.render("Lifes: ", 1, (0, 0, 0),), (550, 6))
        self.screen.blit(
            self.font.render(
                ': {0}'.format(self.points), 1, (0, 0, 0)
            ), (19, 6)
        )
        for i in range(self.lifes):
            self.screen.blit(Game._thumb, (590 + 14 * i, 3))
        self.pieces.draw(self.screen)

    def run(self):
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            keys = pygame.key.get_pressed()
            if keys[K_LCTRL] or keys[K_DOWN]:
                self.hero.shot(self.bullets)
            moving = self.hero.ride(keys)
            for c in self.coins:
                if pygame.sprite.collide_rect(c, self.hero):
                    c.kill()
                    self.points += 1
            for f in pygame.sprite.groupcollide(
                self.foes, self.bullets, False, True
            ):
                f.die()
            pygame.sprite.groupcollide(self.bullets, self.pieces, True, False)
            die = True
            for p in self.pieces:
                if pygame.sprite.collide_rect(p, self.hero):
                    die = False
                    self.hero.collision(p.rect)
            if die and self.hero.die():
                pass
            self.hero.update(self.x >= self.width)
            self.update(moving)
            self.coin.update(True)
            self.draw()
            self.coin.draw(self.screen)
            self.platforms.draw(self.screen)
            self.coins.draw(self.screen)
            self.hero.draw(self.screen)
            self.foes.draw(self.screen)
            self.bullets.draw(self.screen)
            self.exit.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
