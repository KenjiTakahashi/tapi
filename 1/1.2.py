# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480))
size = 10
circle_color = (15, 255, 70)
pos = (0, 0)

background = pygame.Surface(screen.get_size())

for x in range(641):
    #  points...
    for y in range(281):
        r, g, b = 120, abs(0.4 * x % 255), abs(0.9 * y % 255)
        background.set_at((x, y), (r, g, b))
    #  lines...
    pygame.draw.line(background, (0, x % 135, x % 130), (x, 281), (x, 480))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEMOTION:
            c = screen.get_at(event.pos)
            circle_color = (c.b, c.r, c.g, c.a)
            size = event.pos[0] / 20 + event.pos[1] / 20
            pos = (event.pos[0] - size, event.pos[1] - size)
    screen.blit(background, (0, 0))
    pygame.draw.circle(screen, circle_color, pos, size)
    pygame.display.update()
