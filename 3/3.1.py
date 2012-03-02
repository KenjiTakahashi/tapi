# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import cPickle

try:
    image = cPickle.load(open("pickled_image"))
except IOError:
    image = [64 * [(0, (0, 0, 0))] for i in range(48)]

def update(pos, bit, color, big):
    xm, ym = pos
    x = xm / 10
    y = ym / 10
    if x >= 0 and x < 64 and y >= 0 and y < 48:
        image[y][x] = (bit, color)
        if big:
            try:
                for i in range(3):
                    for j in range(3):
                        image[y + i][x + j] = (bit, color)
            except IndexError:
                pass

pygame.init()
screen = pygame.display.set_mode((640, 480))
preview = pygame.Surface((64, 48))
preview_enabled = False
bigger = pygame.Surface((30, 30))
bigger.fill((181, 173, 173))

points = list()

moving = False
bit = 1
big = False
colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]
color = (0, 0, 0)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            cPickle.dump(image, open("pickled_image", "w"))
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                bit = 1
            elif event.button == 3:
                bit = 0
            update(event.pos, bit, color, big)
            moving = True
        if event.type == MOUSEMOTION:
            if moving:
                update(event.pos, bit, color, big)
        if event.type == MOUSEBUTTONUP:
            moving = False
        if event.type == KEYDOWN:
            if event.key == K_LSHIFT:
                big = True
            elif event.key == K_SPACE:
                preview_enabled = True
            else:
                try:
                    color = colors[event.key - 48]
                except IndexError:
                    pass
        if event.type == KEYUP:
            if event.key == K_LSHIFT:
                big = False
            elif event.key == K_SPACE:
                preview_enabled = False
    screen.fill((255, 255, 255))
    if preview_enabled:
        preview.fill((255, 255, 255))
        pygame.draw.rect(preview, (0, 0, 0), ((0, 0), preview.get_size()), 1)
    for i in range(48):
        for j in range(64):
            img_ = image[i][j]
            if img_[0]:
                pygame.draw.rect(screen, img_[1], (10 * j, 10 * i, 10, 10))
                if preview_enabled:
                    pygame.draw.line(preview, img_[1], (j, i), (j, i))
                    #pygame.draw.rect(preview, (0, 0, 0), (j, i, 1, 1)) # WTF?!
    if preview_enabled:
        screen.blit(preview, (0, 432))
    if big:
        x_, y_ = pygame.mouse.get_pos()
        screen.blit(bigger, (x_ - 10, y_ - 10))
    pygame.display.update()
