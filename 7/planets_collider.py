# -*- coding: utf-8 -*-
# Karol "Kenji Takahashi" Wozniak (C) 2012
# GFX by Roencia Game Creators (http://www.roencia.com)

import pygame
from pygame.locals import QUIT, K_UP, K_LEFT, K_RIGHT
from sys import exit
from random import randint
import math


class Sun(pygame.sprite.Sprite):
    def __init__(self):
        super(Sun, self).__init__()


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
        self.x += math.sin(move_angle) * 48
        self.y += math.cos(move_angle) * 48
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

    def _rotate(self, angle):
        oldc = self.rect.center
        self.image = pygame.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldc

    def update(self):
        if not self.died:
            self._rotate(self.angle)
            self.x += math.sin(self.move_angle) * self.acc
            self.y -= math.cos(self.move_angle) * self.acc
        else:
            pass
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if self.move:
            self.flame.update(self.angle, (self.x, self.y))

    def ride(self, key):
        if key[K_UP]:
            self.move = True
            if self.acc < 5:
                self.acc += 0.5
            self.move_angle = -math.radians(self.angle)
        else:
            self.move = False
            if self.acc > 0:
                self.acc -= 0.01
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
        x = self.x % self.size_x
        y = self.y % self.size_y
        self.screen.blit(
            self.image, (0, 0), (x, 0, self.size_x - x, self.size_y - y)
        )
        if x:
            self.screen.blit(
                self.image, (self.size_x - x, y),
                (0, 0, self.size_x, self.size_y)
            )
        if y:
            self.screen.blit(
                self.image, (x, self.size_y - y),
                (0, 0, self.size_x, self.size_y)
            )

    def reset(self):
        self.x = 0
        self.y = 0
        #TODO: Check rand for planets collisions
        self.hero = Ship((randint(40, 600), randint(40, 400)))

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
            self.hero.update()
            self.hero.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
