# -*- coding: utf-8 -*-
# Karol "Kenji Takahashi" Wozniak (C) 2012
# GFX by David Gervais (http://forum.thegamecreators.com/?m=forum_view&t=67876&b=1)

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


class Alien(pygame.sprite.Sprite):
    _invaders = _makeInvaders()

    def __init__(self, position, bullets, special=False):
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
        self.worth = self.type + 1

    def update(self):
        self.x += self.state
        self.tmpAni += 1
        if self.tmpAni > 7:
            self.ani = (self.ani + 1) % 2
            self.tmpAni = 0
        self.image = Alien._invaders[self.type][self.ani]
        if self.x % 640 == 0:
            self.state = -self.state
            self.y += 4
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if randint(0, 900) == 0:
            self.fire()

    def fire(self):
        vx, vy = 0, 4
        self.bullets.add(Bullet(
            (self.rect.centerx + 3 * vx, self.rect.centery + 3 * vy),
            vx, vy
        ))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


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
        self.lifes = 3
        self.setType(1)

    def setType(self, type):
        self.type = type
        self.dy = self.type * 10
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
            vx = 0
            vy = -4
            if self.type == 1:
                self.bullets.add(Bullet(
                    (self.rect.centerx + 3 * vx,
                    self.rect.centery + 3 * vy),
                    vx, vy
                ))
            elif self.type == 2:
                pass
            elif self.type == 3:
                pass
            self.wait = 10

    def hit(self):
        self.destroyed = 1
        self.lifes -= 1
        if self.lifes == 0:
            pass # game over

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
    def __init__(self, position, vx, vy):
        super(Bullet, self).__init__()
        self.x, self.y = position
        self.vx, self.vy = vx, vy
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
        self.x += self.vx
        self.y += self.vy
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        super(Scoreboard, self).__init__()
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
        self.ship = Ship((280, 440), self.rockets)
        self.aliens = self.doAliens()
        self.invaders = pygame.sprite.Group(self.aliens)
        self.update()

    def doAliens(self):
        return [
            Alien((50 * i, 60 + 30 * j), self.bullets)
            for i in range(15) for j in range(4)
        ]

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
            colls = pygame.sprite.groupcollide(
                self.invaders, self.rockets, True, True
            )
            if colls:
                self.update(points=sum([a.worth for a in colls]))
                # play a sound
            self.draw()
            self.invaders.update()
            self.ship.update()
            self.invaders.draw(self.screen)
            self.ship.draw(self.screen)
            self.bullets.update()
            self.rockets.update()
            self.bullets.draw(self.screen)
            self.rockets.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    scoreboard = Scoreboard()
    scoreboard.run()
