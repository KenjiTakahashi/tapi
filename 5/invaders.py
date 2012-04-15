# -*- coding: utf-8 -*-
# Karol "Kenji Takahashi" Wozniak (C) 2012
# GFX by David Gervais (http://forum.thegamecreators.com/?m=forum_view&t=67876)

import pygame
from pygame.locals import *
from sys import exit
from random import randint


def _makeInvaders():
    invaders = list()
    image = pygame.image.load('gfx/inv.png')
    for i in range(3):
        internal = list()
        for j in range(2):
            img = pygame.Surface((24, 24))
            img.blit(image, (0, 0), (j * 24, i * 24, 24, 24))
            img.set_colorkey((255, 0, 255))
            internal.append(img)
        invaders.append(internal)
    return invaders


def _makeShips():
    ships = list()
    image = pygame.image.load('gfx/fighter.png')
    for i in range(3):
        img = pygame.Surface((32, 32))
        img.blit(image, (0, 0), (i * 32, 0, 32, 32))
        img.set_colorkey((255, 0, 255))
        thumb = pygame.transform.scale(img, (14, 14))
        ships.append((img, thumb))
    return ships


def _makeDrops():
    drops = list()
    image = pygame.image.load('gfx/fighter.png')
    for i in range(3):
        img = pygame.Surface((32, 32))
        img.blit(image, (0, 0), (i * 32, 0, 32, 32))
        img.set_colorkey((255, 0, 255))
        drops.append(pygame.transform.scale(img, (14, 14)))
    img = pygame.Surface((20, 20))
    img.fill((90, 90, 90))
    drops.append(img)
    return drops


class Alien(pygame.sprite.Sprite):
    _invaders = _makeInvaders()

    def __init__(self, position, bullets, drops):
        super(Alien, self).__init__()
        self.x, self.y = position
        self.state = 1
        self.type = randint(0, 2)
        self.ani = 0
        self.tmpAni = 0
        self.image = Alien._invaders[self.type][self.ani]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.bullets = bullets
        self.drops = drops
        self.worth = self.type + 1
        self.loading = 50
        self.vy = 4

    def update(self):
        self.tmpAni += 1
        if self.tmpAni > 7:
            self.ani = (self.ani + 1) % 2
            self.tmpAni = 0
        self.image = Alien._invaders[self.type][self.ani]
        if self.loading:
            self.loading -= 1
            self.x += 4
            self.y += 4
        else:
            self.x += self.state
            if self.x % 640 == 0:
                self.state = -self.state
                self.y += 4
            if randint(0, 900) == 0:
                self.fire()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def fire(self):
        self.bullets.add(Bullet(
            (self.rect.centerx, self.rect.centery + 3 * self.vy), self.vy
        ))

    def drop(self):
        self.drops.add(Drop(
            (self.rect.centerx, self.rect.centery + 3 * self.vy), self.vy
        ))


class Ship(pygame.sprite.Sprite):
    _ships = _makeShips()

    def __init__(self, position, bullets):
        super(Ship, self).__init__()
        self.x, self.y = position
        self.dx, self.dy = 0, 0
        self.rect = None
        self.destroyed = 0
        self.bullets = bullets
        self.wait = 0
        self.setType(1)

    def setType(self, type):
        self.type = type
        self.dy = self.type * 20
        self.image = Ship._ships[self.type - 1][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def getThumb(self):
        return Ship._ships[self.type - 1][1]

    def update(self):
        self.x += self.dx
        self.rect.centerx = self.x
        if self.wait > 0:
            self.wait -= 1

    def fire(self):
        if self.wait == 0:
            vy = -4
            if self.type in [1, 3]:
                self.bullets.add(Bullet(
                    (self.rect.centerx, self.rect.centery + 3 * vy), vy
                ))
            if self.type in [2, 3]:
                self.bullets.add(Bullet(
                    (self.rect.centerx - 8, self.rect.centery + 5 * vy), vy
                ))
                self.bullets.add(Bullet(
                    (self.rect.centerx + 8, self.rect.centery + 5 * vy), vy
                ))
            self.wait = 10

    def hit(self):
        self.destroyed = 1

    def reward(self, type):
        if type == 4:
            return True
        self.setType(type)

    def drive(self, key):
        self.dx = 0
        if key[K_LEFT] and self.x > 10:
            self.dx = -4
        if key[K_RIGHT] and self.x < 630:
            self.dx = 4
        if key[K_SPACE]:
            self.fire()

    def up(self):
        self.y -= self.dy
        self.rect.centery = self.y

    def down(self):
        self.y += self.dy
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, vy):
        super(Bullet, self).__init__()
        self.x, self.y = position
        self.vy = vy
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        pygame.draw.circle(self.image, (0, 0, 0), (3, 3), 2)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self):
        if self.y < 0 or self.y > 454:
            self.kill()
        self.y += self.vy
        self.rect.centery = self.y


class Concrete(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Concrete, self).__init__()
        self.x, self.y = position
        self.image = pygame.Surface((5, 5))
        self.image.fill((90, 90, 90))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y


class Wall(list):
    def __init__(self):
        super(Wall, self).__init__()
        self.x = 0
        self.ex = set()

    def create(self):
        brick = pygame.sprite.Group()
        if self.ex:
            self.x = self.ex.pop()
        else:
            self.x += 20
        for i in range(4):
            for j in range(self.x - 20, self.x, 5):
                brick.add(Concrete((j, 380 + i * 5)))
        self.append(brick)

    def update(self):
        for brick in self:
            brick.update()

    def draw(self, screen):
        for brick in self:
            brick.draw(screen)

    def groupcollide(self, one):
        for brick in self:
            res = pygame.sprite.groupcollide(brick, one, True, True)
            if not len(brick):
                x = res.keys()[0].x
                x -= (x % 20)
                self.ex.add(x)
                self.remove(brick)


class Drop(pygame.sprite.Sprite):
    _drops = _makeDrops()

    def __init__(self, position, vy):
        super(Drop, self).__init__()
        self.x, self.y = position
        if randint(0, 3) == 0:
            self.type = randint(0, 2)
        else:
            self.type = 3
        self.image = Drop._drops[self.type]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.vy = vy

    def update(self):
        if self.y > 454:
            self.kill()
        self.y += self.vy
        self.rect.centery = self.y

    def reward(self):
        return self.type + 1


class Board(pygame.sprite.Sprite):
    def __init__(self):
        super(Board, self).__init__()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.level = 1
        self.points = 0
        self.lifes = 3
        self.image = pygame.Surface((640, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centery = 470
        self.font = pygame.font.Font(None, 18)
        self.rockets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        self.wall = Wall()
        self.ship = Ship((280, 440), self.rockets)
        self.doAliens()
        self.update()

    def doAliens(self):
        self.invaders = pygame.sprite.Group([
            Alien((50 * i - 200, 30 * j - 140), self.bullets, self.drops)
            for i in range(13) for j in range(self.level + 3)
        ])

    def update(self, points=0, lifes=0):
        self.points += points
        self.lifes -= lifes
        self.image.fill((255, 255, 255))
        self.image.blit(
            self.font.render("Points: " + str(self.points), 1, (0, 0, 0)),
            (10, 5)
        )
        self.image.blit(
            self.font.render("Lifes: ", 1, (0, 0, 0)), (540, 5)
        )
        thumb = self.ship.getThumb()
        for i in range(self.lifes):
            self.image.blit(thumb, (576 + i * 14, 3))
        if not self.lifes:
            self.image.blit(
                self.font.render("GAME OVER", 1, (0, 0, 0)), (260, 5)
            )

    def draw(self):
        self.screen.blit(self.image, (self.rect.left, self.rect.top))

    def run(self):
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN and event.key == K_UP:
                    self.ship.up()
                if event.type == KEYUP and event.key == K_UP:
                    self.ship.down()
            keys = pygame.key.get_pressed()
            self.screen.fill((60, 90, 250))
            self.ship.drive(keys)
            for b in self.bullets:
                if pygame.sprite.collide_rect(b, self.ship):
                    b.kill()
                    self.ship.hit()
                    self.update(lifes=1)
                    # play a sound
            if self.lifes:
                colls = pygame.sprite.groupcollide(
                    self.invaders, self.rockets, True, True
                )
                self.wall.groupcollide(self.rockets)
                self.wall.groupcollide(self.bullets)
                for d in self.drops:
                    if pygame.sprite.collide_rect(d, self.ship):
                        d.kill()
                        if self.ship.reward(d.reward()):
                            self.wall.create()
                        else:
                            self.update()
                if colls:
                    self.update(points=sum([a.worth for a in colls]))
                    if randint(0, 0) == 0:
                        colls.keys()[randint(0, len(colls) - 1)].drop()
                    # play a sound
                if not self.invaders:
                    self.level += 1
                    self.doAliens()
                self.invaders.update()
                self.ship.update()
                self.invaders.draw(self.screen)
                self.ship.draw(self.screen)
                self.drops.update()
                self.bullets.update()
                self.rockets.update()
                self.wall.update()
                self.drops.draw(self.screen)
                self.bullets.draw(self.screen)
                self.rockets.draw(self.screen)
                self.wall.draw(self.screen)
            self.draw()
            pygame.display.update()


if __name__ == '__main__':
    scoreboard = Board()
    scoreboard.run()
