# -*- coding: utf-8 -*-
"""
SoftwareDesign HW6 - Video Game
Olin Snowman: A game for protecting Olin Snowman from Babsoners!

Created on Fri Mar  7 20:18:57 2014

@author:
    SeongHyeok Im
    Shrinidhi Thirumalai
    Inseong Joe

@note:
    Code-style:
        - Camelcase for function and class.
        - Underscore for variable.
        - Prefix 'g_' for global viarlable.
"""

############################################################################
# Imports
############################################################################

import pygame
from pygame.locals import *
import random
import math
import time
import sys, traceback

############################################################################
# Global configurations
############################################################################

g_snowman_width = 60
g_snowman_height = 80

g_babsoner_width = 60
g_babsoner_height = 30
g_babsoner_vy = 5

############################################################################
# Model Classes
############################################################################

class SnowManModel:
    """ Encodes overall game state of Snowman game """
    def __init__(self):
        # initialize
        self.babsoners = []
        self.snowman = SnowMan(g_snowman_width,
                               g_snowman_height,
                               (screen.get_width() / 2 - g_snowman_width / 2),
                               (screen.get_height() - g_snowman_height),
                               0,
                               3)
        self.score = 0
        self.snowman.PrintAll()

    def CreateBabsoner(self, vy): #set velocity in controller
        #a = random.randint(50, 150) #sets random width of babsoner
        #babson = Babsoner(a, a * 2, random.randint(int(a / 2.0), int(640 - a /2.0)), 0, vy, 0)
        babson = Babsoner(g_babsoner_width, g_babsoner_height, random.randint(100, 500), 0, g_babsoner_vy, True)
        self.babsoners.append(babson)
        print "Babsoner Created!"

    def RemoveBabsoner(self, babsoner):
        babsoner.is_visible = 1

    def GetScore(self,num_rmvd_babsoners, ellapsed_time):
        self.score += num_rmvd_babsoners+ellapsed_time

    def update(self):
        self.snowman.update()
        self.score.update()

class SnowMan:
    """ Encodes state of snowman """
    def __init__(self, width, height, x, y, vx, lives):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vx = vx
        self.lives = lives
        self.image = pygame.transform.scale(pygame.image.load("./snowman.png"), (self.width, self.height))

    def PrintAll(self):
        print "== Snowman =="
        print "width:", self.width
        print "height:", self.height
        print "x:", self.x
        print "y:", self.y
        print "vx:", self.vx
        print "lives:", self.lives
        print "============="

class Babsoner:
    """Encodes state of babsoner"""
    def __init__(self, width, height, x, y, vy, is_visible):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vy = vy
        self.is_visible = is_visible
        self.image = pygame.transform.scale(pygame.image.load("./babsoner.png"), (self.width, self.height))
        # this works on images with per pixel alpha too
        alpha = 255
        self.image.fill((211, 242, 241, alpha), None, pygame.BLEND_RGBA_MULT)

############################################################################
# View Classes
############################################################################

class SnowManView:
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        # Filling Background Color
        self.screen.fill(pygame.Color(211, 242, 241))

        # Displaying Babsoners
        for babsoner in self.model.babsoners:
            if babsoner.is_visible == True:
                #print "Babsoner Displayed!"
                try:
                    screen.blit(babsoner.image, (babsoner.x, babsoner.y))
                except:
                    print "x: %d / y: %d", (babsoner.x, babsoner.y)
                    traceback.print_exc(file=sys.stdout)
                    sys.exit(1)
                #pygame.display.flip()

        # Displaying Snowman
        screen.blit(self.model.snowman.image, (model.snowman.x, model.snowman.y))
        pygame.display.flip()

############################################################################
# Controller Classes
############################################################################

class SnowManMouseController:
    """ """
    def __init__(self, model):
        self.model = model

    def HandleMouseEvent(self, event):
        if event.type == MOUSEMOTION:
            self.model.snowman.x = event.pos[0] - (self.model.snowman.width / 2.0)

class SnowManBabsonerController:
    """ """
    def __init__(self, model):
        self.model = model

    def update(self):
        """ """
        for babsoner in self.model.babsoners:
            babsoner.y += babsoner.vy

    def create(self):
        """ """
        self.model.CreateBabsoner(g_babsoner_vy)

class SnowManCollisionController:
    """ """
    def __init__(self, model):
        self.model = model

    def check(self):
        pass

############################################################################
# Main
############################################################################

if __name__ == "__main__":
    pygame.init()

    size = (640, 480)
    screen = pygame.display.set_mode(size)

    model = SnowManModel()
    view = SnowManView(model, screen)
    controller_mouse = SnowManMouseController(model)
    controller_babsoner = SnowManBabsonerController(model)
    controller_collision = SnowManCollisionController(model)

    pygame.time.set_timer(USEREVENT + 1, 50)
    pygame.time.set_timer(USEREVENT + 2, 1000)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEMOTION:
                controller_mouse.HandleMouseEvent(event)
            if event.type == USEREVENT + 1:
                controller_babsoner.update()
                controller_collision.check()
            if event.type == USEREVENT + 2:
                controller_babsoner.create()
        view.draw()
        time.sleep(.001)

    pygame.quit()
