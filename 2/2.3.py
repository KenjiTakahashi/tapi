# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import os

pygame.init()
screen = pygame.display.set_mode((1366, 768))
toolbox = pygame.Surface((326, 3468))
toolbox.fill((21, 33, 187))
pygame.draw.line(toolbox, (110, 116, 200), (323, 0), (323, 3568), 6)
blocks = dict()
x, y = 5, 5
for file in os.listdir('cute'):
    image = pygame.image.load(os.path.join('cute', file)).convert_alpha()
    toolbox.blit(image, (x, y))
    blocks[(x, y)] = image
    x = (x + 106) % 318
    if x == 5:
        y += 176
board = pygame.Surface((1040, 768))
composition = dict()
#  read it from file, yeah!
clock = pygame.time.Clock()
dy = 0
block = None
active_block_pos = (0, 0)
block_pos = (0, 0)
moving = False
rect_x, rect_y = None, None

def get_block(dy, point):
    point = (point[0], point[1] + dy)
    for coord, block in blocks.iteritems():
        if pygame.Rect(coord, (101, 171)).collidepoint(point):
            return (block, coord)
    return (None, None)

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                if dy > 0 and event.pos[0] < 328:
                    dy -= 50
                #toolbox.scroll(0, 50)
            elif event.button == 5:
                if dy < 2668 and event.pos[0] < 328:
                    dy += 50
                #toolbox.scroll(0, -50)
            elif event.button == 1:
                block, block_pos = get_block(dy, event.pos)
                active_block_pos = (event.pos[0] - 50, event.pos[1] - 85)
                if block:
                    moving = True
        if event.type == MOUSEMOTION and moving:
            x_ = event.pos[0]
            y_ = event.pos[1]
            rect_x = (x_ - 328) / 101 * 101
            rect_y = y_ / 171 * 171
            active_block_pos = (x_ - 50, y_ - 85)
        if event.type == MOUSEBUTTONUP and moving:
            composition[(rect_x, rect_y)] = block_pos
            block = None
            moving = False
            rect_x, rect_y = None, None
    screen.blit(toolbox, (0, 0), (0, dy, 326, 768))
    screen.blit(board, (326, 0))
    board.fill((32, 120, 38))
    if rect_x != None and rect_y != None:
        pygame.draw.rect(board, (59, 168, 231), (rect_x, rect_y, 101, 171))
    for coord, block_ in composition.iteritems():
        board.blit(blocks[block_], dest=coord)
    if block:
        screen.blit(block, active_block_pos)
    pygame.display.update()
