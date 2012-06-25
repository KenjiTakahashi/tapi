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

    def update(self, lifes, life, shield, fuel, points=0):
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
        if shield:
            pygame.draw.line(
                self.image, (180, 170, 30), (25, 44), (25 + shield, 44), 8
            )
        self.image.blit(self.font.render('F:', 1, (0, 0, 0)), (10, 55))
        if fuel:
            pygame.draw.line(
                self.image, (0, 20, 200), (25, 59), (25 + fuel, 59), 8
            )

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


def _makeAni(name, n):
    ani = list()
    for i in range(n):
        img = pygame.image.load('gfx2/{0}-{1}.png'.format(name, i))
        ani.append(img)
    return ani


class Fuel(pygame.sprite.Sprite):
    _fuel = _makeAni('c', 50)

    def __init__(self):
        super(Fuel, self).__init__()
        self.x, self.y = randint(20, 780), randint(20, 580)
        self.ani = 0
        self.wait = 140
        self.image = Fuel._fuel[self.ani].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self):
        self.ani += 1
        self.ani %= 25
        self.image = Fuel._fuel[self.ani].convert_alpha()
        self.wait -= 1
        if not self.wait:
            self.kill()


class SuperShield(pygame.sprite.Sprite):
    _sshield = _makeAni('ss', 50)

    def __init__(self):
        super(SuperShield, self).__init__()
        self.x, self.y = randint(20, 780), randint(20, 580)
        self.ani = 0
        self.wait = 140
        self.image = SuperShield._sshield[self.ani].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self):
        self.ani += 1
        self.ani %= 50
        self.image = SuperShield._sshield[self.ani].convert_alpha()
        self.wait -= 1
        if not self.wait:
            self.kill()


class Coin(pygame.sprite.Sprite):
    _coin = _makeAni('coin', 25)

    def __init__(self):
        super(Coin, self).__init__()
        self.x, self.y = randint(20, 780), randint(20, 580)
        self.ani = 0
        self.wait = 200
        self.image = Coin._coin[self.ani].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self):
        self.ani += 1
        self.ani %= 25
        self.image = Coin._coin[self.ani].convert_alpha()
        self.wait -= 1
        if not self.wait:
            self.kill()


class Sun(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Sun, self).__init__()
        self.x, self.y = position
        self.diameter = randint(120, 200)
        self.radius = self.diameter / 2
        self.image = pygame.image.load('gfx2/sun.jpg')
        self.orig = self.image
        self.reimage()

    def burn(self):
        self.diameter -= 1
        self.radius -= 0.5
        self.reimage()

    def reimage(self):
        self.image = pygame.transform.scale(
            self.orig, (self.diameter, self.diameter)
        )
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def collide(self, item):
        try:
            x, y = item
        except TypeError:
            if pygame.sprite.collide_circle(self, item):
                return 1.0
            elif pygame.sprite.collide_circle_ratio(1.3)(self, item):
                return 0.5
            return 0.0
        else:
            return self.rect.colliderect(
                pygame.rect.Rect((x - 32, y - 32), (96, 96))
            )

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Planet(pygame.sprite.Sprite):
    def __init__(self, sun):
        super(Planet, self).__init__()
        self.diameter = randint(50, 150)
        self.radius = self.diameter / 2
        self.mass = self.diameter / 4
        self.image = pygame.image.load(
            'gfx2/planets/{0}.png'.format(randint(1, 19))
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.diameter, self.diameter)
        )
        self.rect = self.image.get_rect()
        self.sun = sun

    def update(self):
        self.degree += 1
        self.degree %= 360
        self.x = math.cos(self.degree * 2 * math.pi / 360) * self.xradius
        self.y = math.sin(self.degree * 2 * math.pi / 360) * self.yradius
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def reset(self):
        self.degree = randint(0, 360)
        while True:
            x = randint(110, 600)
            y = randint(110, 600)
            # FIXME: needs re-thinking
            if(pygame.Rect(-x, -y, 2 * x, 2 * y).contains(self.sun.rect)):
                self.xradius = x
                self.yradius = y
                break


class Flame(pygame.sprite.Sprite):
    _flames = _makeAni('flame', 50)

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


class SuperShieldShape(pygame.sprite.Sprite):
    def __init__(self, position):
        super(SuperShieldShape, self).__init__()
        self.x, self.y = position
        self.image = pygame.Surface((64, 64))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, (160, 90, 20), (32, 32), 24, 3)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self, pos):
        self.x, self.y = pos
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Ship(pygame.sprite.Sprite):
    def __init__(self, *func):
        super(Ship, self).__init__()
        self.image = pygame.image.load('gfx2/p.gif').convert_alpha()
        self.orig = self.image  # for rotation
        self.rect = self.image.get_rect()
        self.died = False
        self.move = False
        self.angle = 0
        self.move_angle = 0
        self.acc = 0
        self.life = 100
        self.lifes = 3
        self.shield = 100
        self.fuel = 100
        self.sshield = 0
        self.sshieldshape = None
        self.wait = 0
        self.collide_func = func

    def _rotate(self, angle):
        oldc = self.rect.center
        self.image = pygame.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect()
        self.rect.center = oldc

    def refuel(self):
        if self.fuel < 100:
            self.fuel += 10
            if self.fuel > 100:
                self.fuel = 100

    def supershield(self):
        self.sshield = 80
        self.sshieldshape = SuperShieldShape(
            (self.rect.centerx, self.rect.centery)
        )

    def update(self, suncollide):
        if suncollide == 1.0 and not self.sshield:
            self.died = True
        elif suncollide and not self.sshield:
            self.wait = -50
            if self.shield:
                self.shield -= 5
            else:
                self.life -= 2
            if not self.life:
                self.died = True
        else:
            self.wait += 1
            if self.wait == 20:
                self.wait = 0
                if self.shield < 100:
                    self.shield += 5
        if not self.died:
            self._rotate(self.angle)
            self.x += math.sin(self.move_angle) * self.acc
            self.y -= math.cos(self.move_angle) * self.acc
        else:
            self.lifes -= 1
            if self.lifes:
                self.reset()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if self.sshield:
            self.sshieldshape.update((self.rect.centerx, self.rect.centery))
            self.sshield -= 1
        elif self.sshieldshape:
            self.sshieldshape.kill()
            self.sshieldshape = None
        if self.move:
            self.flame.update(self.angle, (self.x, self.y))
        return (self.lifes, self.life, self.shield, self.fuel)

    def reset(self):
        self.life = 100
        self.shield = 100
        self.died = False
        found = False
        self.acc = 0
        while not found:
            x = randint(40, 600)
            y = randint(40, 400)
            for f in self.collide_func:
                if not f((x, y)):
                    found = True
                    break
        self.x, self.y = x, y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.flame = Flame((x, y))

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
        if self.sshield:
            self.sshieldshape.draw(screen)


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
        self.hud = HUD()

    def draw(self):
        self.screen.blit(self.image, (0, 0))

    def reset(self):
        self.sun = Sun((randint(80, 500), randint(80, 340)))
        self.planets = pygame.sprite.Group()
        for i in range(randint(1, 5)):
            planet = Planet(self.sun)
            planet.reset()
            self.planets.add(planet)
        self.fuel = pygame.sprite.Group()
        self.sshield = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.hero = Ship(self.sun.collide)
        self.hero.reset()

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
            scollide = self.sun.collide(self.hero)
            lifes, life, shield, fuel = self.hero.update(scollide)
            if scollide and self.hero.sshield:
                self.sun.burn()
            if not self.sun.diameter:
                self.reset()
                continue
            for fuel_ in pygame.sprite.spritecollide(
                self.hero, self.fuel, False
            ):
                fuel_.kill()
                self.hero.refuel()
            for ss in pygame.sprite.spritecollide(
                self.hero, self.sshield, False
            ):
                ss.kill()
                self.hero.supershield()
            points = len(
                pygame.sprite.spritecollide(self.hero, self.coins, True)
            )
            if not lifes:
                # TODO: game over
                continue
            if not randint(0, 400):
                self.fuel.add(Fuel())
            if not randint(0, 650):
                self.sshield.add(SuperShield())
            if not randint(0, 100):
                self.coins.add(Coin())
            self.fuel.update()
            self.sshield.update()
            self.coins.update()
            self.hud.update(lifes, life, shield, fuel, points)
            self.planets.update()
            self.fuel.draw(self.screen)
            self.sshield.draw(self.screen)
            self.coins.draw(self.screen)
            self.sun.draw(self.screen)
            self.planets.draw(self.screen)
            self.hero.draw(self.screen)
            self.hud.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
