# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
import os
import cPickle

pygame.init()
screen = pygame.display.set_mode((800, 600))
toolbox = pygame.Surface((160, 3468))
toolbox.fill((21, 33, 187))
pygame.draw.line(toolbox, (110, 116, 200), (157, 0), (157, 3468), 6)
blocks = dict()
x, y = 4, 4
for file in os.listdir('cg2'):
    image = pygame.image.load(os.path.join('cg2', file))
    image.set_colorkey((75, 99, 127))
    toolbox.blit(image, (x, y))
    blocks[(x, y)] = image
    x = (x + 44) % 132
    if x == 4:
        y += 44
board = pygame.Surface((574, 600))
clock = pygame.time.Clock()
try:
    composition = cPickle.load(open("pickled_board"))
except IOError:
    composition = dict()
dy = 0
block = None
active_block_pos = (0, 0)
block_pos = (0, 0)
moving = False
rect_x, rect_y = None, None

def get_block(blocks, dy, point):
    point = (point[0], point[1] + dy)
    for coord, block in blocks.iteritems():
        if pygame.Rect(coord, (40, 40)).collidepoint(point):
            return (block, coord)
    return (None, None)

def get_composition_block(dy, point):
    point = (point[0], point[1] + dy)
    for coord, block in composition.iteritems():
        if pygame.Rect(coord, (40, 40)).collidepoint(point):
            return (blocks[block], block, coord)
    return (None, None)

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            cPickle.dump(composition, open("pickled_board", "w"))
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x_ = event.pos[0]
                y_ = event.pos[1]
                if x_ < 160:
                    block, block_pos = get_block(blocks, dy, (x_, y_))
                else:
                    block, block_pos, coord = get_composition_block(
                        dy, (x_ - 160, y_)
                    )
                    if block:
                        del composition[coord]
                active_block_pos = (x_ - 20, event.pos[1] - 20)
                if block:
                    moving = True
        if event.type == MOUSEMOTION and moving:
            x_ = event.pos[0]
            y_ = event.pos[1]
            rect_x = (x_ - 160) / 40 * 40
            rect_y = y_ / 40 * 40
            active_block_pos = (x_ - 20, y_ - 20)
        if event.type == MOUSEBUTTONUP and moving:
            composition[(rect_x, rect_y)] = block_pos
            block = None
            moving = False
            rect_x, rect_y = None, None
    screen.blit(toolbox, (0, 0), (0, dy, 160, 600))
    screen.blit(board, (160, 0))
    board.fill((32, 120, 38))
    if rect_x != None and rect_y != None:
        pygame.draw.rect(board, (59, 168, 231), (rect_x, rect_y, 40, 40))
    for coord, block_ in composition.iteritems():
        board.blit(blocks[block_], coord)
    if block:
        screen.blit(block, active_block_pos)
    pygame.display.update()
