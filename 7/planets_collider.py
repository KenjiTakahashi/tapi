# -*- coding: utf-8 -*-
# Karol "Kenji Takahashi" Wozniak (C) 2012
# GFX by Roencia Game Creators (http://www.roencia.com)

import pygame
from pygame.locals import QUIT, K_UP, K_LEFT, K_RIGHT
from sys import exit
from random import randint
import math


class HUD(pygame.sprite.Sprite):
    def __init__(self):
        super(HUD, self).__init__()
        self.font = pygame.font.Font(None, 16)
        self.image = pygame.Surface((135, 74))
        self.image.set_alpha(200)
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.top = 500
        self.points = 0

    def update(self, lifes, life, points=0):  # FIXME: provide points
        self.points += points
        self.image.fill((100, 100, 100))
        self.image.blit(
            self.font.render(
                'L: {0} P: {1}'.format(lifes, self.points),
                1, (0, 0, 0)
            ), (10, 10)
        )
        self.image.blit(self.font.render('H:', 1, (0, 0, 0)), (10, 25))
        pygame.draw.line(self.image, (90, 0, 0), (25, 29), (25 + life, 29), 8)
        self.image.blit(self.font.render('S:', 1, (0, 0, 0)), (10, 40))
        self.image.blit(self.font.render('F:', 1, (0, 0, 0)), (10, 55))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Sun(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Sun, self).__init__()
        self.x, self.y = position
        self.diameter = randint(120, 200)
        self.radius = self.diameter / 2
        self.image = pygame.image.load('gfx2/sun.jpg')
        self.image = pygame.transform.scale(
            self.image, (self.diameter, self.diameter)
        )
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def collide(self, item):
        try:
            return self.rect.colliderect(pygame.rect.Rect(item, (32, 32)))
            x, y = item
        except TypeError:
            if pygame.sprite.collide_circle(self, item):
                return 1.0
            elif pygame.sprite.collide_circle_ratio(1.3)(self, item):
                return 0.5
            return 0.0

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super(Planet, self).__init__()


def _makeFlames():
    flames = list()
    for i in range(50):
        img = pygame.image.load('gfx2/flame-{0}.png'.format(i))
        flames.append(img)
    return flames


class Flame(pygame.sprite.Sprite):
    _flames = _makeFlames()

    def __init__(self, position):
        super(Flame, self).__init__()
        self.x, self.y = position
        self.image = Flame._flames[0].convert_alpha()
        self.orig = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.angle = 0
        self.ani = 0

    def _rotate(self, angle):
        oldc = self.rect.center
        self.image = pygame.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldc

    def update(self, angle, position):
        self.ani += 1
        self.ani %= 49
        self.image = Flame._flames[self.ani].convert_alpha()
        self.orig = self.image
        self._rotate(angle)
        self.x, self.y = position
        move_angle = math.radians(angle)
        self.x += math.sin(move_angle) * 24
        self.y += math.cos(move_angle) * 24
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Ship(pygame.sprite.Sprite):
    _flames = _makeFlames()

    def __init__(self, position):
        super(Ship, self).__init__()
        self.x, self.y = position
        self.image = pygame.image.load('gfx2/p.gif').convert_alpha()
        self.orig = self.image  # for rotation
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.died = False
        self.move = False
        self.angle = 0
        self.move_angle = 0
        self.acc = 0
        self.flame = Flame(position)
        self.life = 100
        self.lifes = 3

    def _rotate(self, angle):
        oldc = self.rect.center
        self.image = pygame.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldc

    def update(self, suncollide):
        if suncollide == 1.0:
            self.died = True
        elif suncollide:
            self.life -= 10
        if not self.died:
            self._rotate(self.angle)
            self.x += math.sin(self.move_angle) * self.acc
            self.y -= math.cos(self.move_angle) * self.acc
        else:
            self.lifes -= 1
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if self.move:
            self.flame.update(self.angle, (self.x, self.y))
        return self.lifes

    def ride(self, key):
        if key[K_UP]:
            self.move = True
            if self.acc < 5:
                self.acc += 0.5
            self.move_angle = -math.radians(self.angle)
        else:
            self.move = False
            if self.acc > 0:
                self.acc -= 0.02
                if self.acc < 0:
                    self.acc = 0
        if key[K_LEFT]:
            self.angle += 5
        if key[K_RIGHT]:
            self.angle -= 5

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))
        if self.move:
            self.flame.draw(screen)


class Game(pygame.sprite.Sprite):
    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        self.size_x = 800
        self.size_y = 600
        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        self.clock = pygame.time.Clock()
        self.ended = False
        self.image = pygame.image.load('gfx2/b.jpg').convert()
        self.rect = self.image.get_rect()
        self.reset()

    def draw(self):
        self.screen.blit(self.image, (0, 0))

    def reset(self):
        self.sun = Sun((randint(80, 500), randint(80, 340)))
        while True:
            x = randint(40, 600)
            y = randint(40, 400)
            if not self.sun.collide((x, y)):
                break
        self.hero = Ship((x, y))
        self.hud = HUD()

    def run(self):
        while not self.ended:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            if not self.hero.died:
                keys = pygame.key.get_pressed()
                self.hero.ride(keys)
            self.draw()
            lifes = self.hero.update(self.sun.collide(self.hero))
            if not lifes:
                self.reset()
                continue
            self.hud.update(lifes, self.hero.life)
            self.sun.draw(self.screen)
            self.hero.draw(self.screen)
            self.hud.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
