# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import cPickle
from math import hypot

try:
    points = cPickle.load(open("pickled_points"))
except IOError:
    points = list()

pygame.init()
screen = pygame.display.set_mode((640, 480))

moving = False
line_color = (16, 140, 55)
circle_color = (100, 100, 255)
circle_radius = 8
dragger = (0, 0)

def not_in(x, y):
    for (x_, y_) in points:
        if hypot(x_ - x, y_ - y) < circle_radius:
            return (x_, y_)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            cPickle.dump(points, open("pickled_points", "w"))
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            moving = True
            dragger = not_in(event.pos[0], event.pos[1])
            if not dragger:
                points.append(event.pos)
        if event.type == MOUSEBUTTONUP:
            moving = False
        if event.type == MOUSEMOTION:
            if moving:
                points[points.index(dragger)] = event.pos
                dragger = event.pos
    screen.fill((140, 55, 16))
    try:
        for i, (x, y) in enumerate(points[:-1]):
            pygame.draw.circle(screen, circle_color, (x, y), circle_radius)
            pygame.draw.line(screen, line_color, (x, y), points[i + 1], 2)
        pygame.draw.circle(screen, circle_color, points[-1], circle_radius)
    except IndexError: # no points yet
        pass
    pygame.display.update()
