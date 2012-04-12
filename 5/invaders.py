# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
from random import randint


class Alien(pygame.sprite.Sprite):
    def __init__(self, position, bullets, special=False):
        super(Alien, self).__init__()
        self.x, self.y = position
        self.state = 1
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.bullets = bullets

    def update(self):
        self.x += self.state
        if self.x % 640 == 0:
            self.state = -self.state
            self.y += 2
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
    _desa = [None,
        [],
        [],
        []
    ]

    def __init__(self, position, bullets):
        super(Ship, self).__init__()
        self.x, self.y = position
        self.dx, self.dy = 0, 0
        self.image = pygame.Surface((80, 20))
        self.image.set_colorkey((0, 0, 0))
        self.rect = None
        self.destroyed = 0
        self.bullets = bullets
        self.wait = 0
        self.type = 1
        self.lifes = 3
        self._setType()

    def _setType(self):
        self.dy = self.type * 10
        if self.type == 1:
            self.rect = pygame.draw.polygon(self.image, (250, 180, 60),
                [(0, 20), (0, 10), (36, 10), (36, 0),
                (41, 0), (41, 10), (80, 10), (80, 20)]
            )
        elif self.type == 2:
            pass
        elif self.type == 3:
            pass
        else:
            raise ValueError()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def update(self):
        if self.destroyed:
            self.image.fill((0, 0, 0))
            pygame.draw.polygon(self.image, (250, 180, 60),
                self._desa[self.destroyed]
            )
        else:
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
                    (self.rect.centerx - 3 + 3 * vx,
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

    def levelUp(self):
        self.type += 1
        self._setType()

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
        self.x += self.vx
        self.y += self.vy
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        super(Scoreboard, self).__init__()
        self.level = 1
        self.points = 0
        self.lifes = 3
        self.image = pygame.Surface((640, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centery = 470
        self.font = pygame.font.Font(None, 18)
        self.image.blit(
            self.font.render("Points: " + str(self.points), 1, (0, 0, 0)),
            (10, 5)
        )
        self.image.blit(
            self.font.render("Lifes: ", 1, (0, 0, 0)), (540, 5)
        )

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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 480))
scoreboard = Scoreboard()

rockets = pygame.sprite.Group()
bullets = pygame.sprite.Group()

ship = Ship((280, 440), rockets)


def do_aliens():
    return [Alien((50 * i, 20 + 30 * j), bullets)
        for i in range(15) for j in range(4)]
aliens = do_aliens()
invaders = pygame.sprite.Group(aliens)

clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN and event.key == K_UP:
            ship.up()
        if event.type == KEYUP and event.key == K_UP:
            ship.down()
    keys = pygame.key.get_pressed()
    screen.fill((60, 90, 250))
    ship.drive(keys)
    for b in bullets:
        if pygame.sprite.collide_rect(b, ship):
            b.kill()
            ship.hit()
            scoreboard.update(lifes=1)
            # play a sound
    collides = pygame.sprite.groupcollide(rockets, invaders, True, True)
    if collides:
        scoreboard.update(points=len(collides))
        # play a sound
    scoreboard.draw(screen)
    invaders.update()
    ship.update()
    invaders.draw(screen)
    ship.draw(screen)
    bullets.update()
    rockets.update()
    bullets.draw(screen)
    rockets.draw(screen)
    pygame.display.update()
