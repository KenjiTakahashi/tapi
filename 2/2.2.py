# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Rzeznik Drzew")
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.Font(None, 18)

deaths = dict()
adeaths = dict()
for d in ["e", "n", "ne", "nw", "s", "se", "sw", "w"]:
    deaths[d] = [
        pygame.image.load("mdb/w" + d + str(i) + ".png").convert_alpha()
        for i in range(8)
    ]
    adeaths[d] = [
        pygame.image.load("mdb/a" + d + str(i) + ".png").convert_alpha()
        for i in range(12)
    ]


direction = "e"
which = 0
x = 0
y = 0
points = 0

trees_tmp = pygame.image.load("mdb/trees.png").convert_alpha()
trees = list()
for i in range(4):
    for j in range(8):
        trees.append(trees_tmp.subsurface((i * 128, j * 128, 128, 128)))
active_trees = [
    (randint(0, 31), (randint(0, 450), randint(0, 400)))
    for i in range(10) if randint(0, 10) <= i
]

def render_trees(points):
    for (i, pos) in active_trees:
        screen.blit(trees[i], pos)
    screen.blit(font.render(str(points), 1, (255, 255, 255)), (10, 460))

def move():
    screen.fill((106, 76, 48))
    render_trees(points)
    screen.blit(deaths[direction][which], (x, y))
    pygame.display.update()
move()

def attack(points):
    player = pygame.Rect(x + 32, y + 32, 96, 96)
    for i, (_, pos) in enumerate(active_trees):
        if player.colliderect(pygame.Rect(tuple(a + 32 for a in pos), (96, 96))):
            del active_trees[i]
            points += 1
    for i in range(12):
        clock.tick(30)
        screen.fill((106, 76, 48))
        render_trees(points)
        screen.blit(adeaths[direction][i], (x, y))
        pygame.display.update()
    return points

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    key = pygame.key.get_pressed()
    new_direction = ""
    if key[K_UP]:
        new_direction = "n"
        if y > -32:
            y -= 2
    elif key[K_DOWN]:
        new_direction = "s"
        if y < 384:
            y += 2
    if key[K_RIGHT]:
        new_direction += "e"
        if x < 544:
            x += 2
    elif key[K_LEFT]:
        new_direction += "w"
        if x > -32:
            x -= 2
    if new_direction:
        which += 1
        which %= 8
        direction = new_direction
        move()
    if key[K_SPACE]:
        points = attack(points)
