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

############################################################################
# Model Classes
############################################################################

snowman_width = 60
snowman_height = 80

class SnowManModel:
    """ Encodes overall game state of Snowman game """
    def __init__(self):
        # initialize
        self.babsoners = []
        self.snowman = SnowMan(snowman_width,
                               snowman_height,
                               (screen.get_width() / 2 - snowman_width / 2),
                               (screen.get_height() - snowman_height),
                               0,
                               3)
        self.score = 0

    def CreateBabsoner(self,vy): #set velocity in controller
        a = random.randint(50,150) #sets random width of babsoner
        babson = Babsoner(a,a*2,random.randint(a/2.0,640-a/2.0),0,vy,0)
        self.babsoner.append(babson)

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
        #inputs:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vx = vx #velocity in x direction
        self.lives = lives #number of lives

class Babsoner:
    """Encodes state of babsoner"""
    def __init__(self, width, height, x, y, vy, is_visible):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vy = vy
        self.is_visible = is_visible

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
            if babsoner.is_visible == 0:
                image = pygame.image.load("babsoner.png")
                pygame.transform.scale(image, (babsoner.width, babsoner.height)) #scales image to height and width
                image_rect = image.get_rect() #gets x and y coordinates of image
                image_rect.x = image.x #moves image to x and y location input:
                image_rect.y = image.y
                screen.blit(image, image_rect)
                pygame.display.flip()
        #Displaying Snowman
        image = pygame.image.load("snowman.png")
        pygame.transform.scale(image, (self.model.snowman.width, self.model.snowman.height)) #scales image to height and width
        image_rect = image.get_rect()
        image_rect.x = model.snowman.x
        image_rect.y = model.snowman.y
        screen.blit(image, image_rect)
        pygame.display.flip()

############################################################################
# Controller Classes
############################################################################

class SnowManMouseController:
    """ """
    def __init__(self, model):
        self.model = model

    def HandleMouseEvent(self, event):
        pass

class SnowManBabsonerController:
    """ """
    def __init__(self, model):
        self.model = model

class SnowManCollisionController:
    """ """
    def __init__(self, model):
        self.model = model

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

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEMOTION:
                controller_mouse.HandleMouseEvent(event)
        #model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
