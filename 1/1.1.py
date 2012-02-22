# -*- coding: utf-8 -*-

import pygame
from pygame.locals import QUIT, MOUSEMOTION
from math import hypot

pygame.init()
screen = pygame.display.set_mode((640, 480))
pixels = 1000
points = []

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == MOUSEMOTION:
            points.append(event.pos)
            while sum([hypot(x1 - x2, y1 - y2)
                for (x1, y1), (x2, y2) in zip(points[0:], points[1:])
            ]) > pixels:
                del points[0]
    screen.fill((255, 255, 255))
    if len(points) > 2:
        pygame.draw.lines(screen, (70, 255, 70), False, points, 2)
    pygame.display.update()
