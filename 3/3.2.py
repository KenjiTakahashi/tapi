# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Riding")
clock = pygame.time.Clock()

background = pygame.image.load("tatry2razy.jpg").convert()
width = background.get_width()

start = 0
body_upper = (300, 360)
body_lower = (300, 400)
left_hand_x = 300
left_hand_y = 375
right_hand_x = 300
right_hand_y = 375
sign = 1
hand_pos = 0

class Leg(object):
    def __init__(self):
        self.x = 300
        self.y = 415
        self.mid_x = 302
        self.mid_y = 406
        self.end_x = 300
        self.end_y = 413
        self.frame = 10

    def draw(self, start, screen):
        if self.x == 285 or self.x == 315 or self.x == 300:
            pygame.draw.line(screen, (0, 0, 0), start, (self.x, self.y), 2)
        else:
            pygame.draw.line(
                screen, (0, 0, 0), start,
                (self.mid_x, self.mid_y), 2
            )
            pygame.draw.line(
                screen, (0, 0, 0),
                (self.mid_x, self.mid_y),
                (self.end_x, self.end_y), 2
            )

    def tick(self, sign):
        self.x += sign * 1
        if self.frame >= 5:
            self.mid_y += 1
            self.mid_x -= 1
        else:
            self.mid_y -= 1
            self.mid_x += 1
        self.end_x += 1
        self.end_y -= 1
        self.frame = (self.frame + 1) % 20

left_leg = Leg()
right_leg = Leg()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    key = pygame.key.get_pressed()
    if key[K_LEFT]:
        start += 2
        if hand_pos == 10:
            sign = 1
        elif hand_pos == -10:
            sign = -1
        hand_pos -= sign * 1
    elif key[K_RIGHT]:
        start -= 2
        if hand_pos == 10:
            sign = -1
        elif hand_pos == -10:
            sign = 1
        hand_pos += sign * 1
        left_leg.tick(sign)
    screen.blit(background, (start, 0))
    screen.blit(background, (start - width, 0))
    pygame.draw.line(screen, (0, 0, 0), body_upper, body_lower, 2)
    pygame.draw.line(
        screen, (0, 0, 0), body_upper,
        (
            left_hand_x + hand_pos,
            left_hand_y - (hand_pos < 0 and -hand_pos or hand_pos) / 2
        ), 2
    )
    pygame.draw.line(
        screen, (0, 0, 0), body_upper,
        (
            right_hand_x - hand_pos,
            right_hand_y - (hand_pos < 0 and -hand_pos or hand_pos) / 2
        ), 2
    )
    left_leg.draw(body_lower, screen)
    pygame.display.update()
