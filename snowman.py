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
# Global variabless
############################################################################

g_screen_width = 640
g_screen_height = 480

g_snowman_width = 60
g_snowman_height = 120

g_babsoner_width = 70
g_babsoner_height = 50
g_babsoner_vy = 10

g_max_babsoner = 10
g_num_rmvd_babsoners = 0

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
                               (g_screen_width / 2 - g_snowman_width / 2),
                               (g_screen_height - g_snowman_height),
                               0,
                               3)
        self.score = 0
        self.snowman.printAll()

    def createBabsoner(self, vy):
        if len(self.babsoners) < g_max_babsoner:
            babson = Babsoner(g_babsoner_width,
                              g_babsoner_height,
                              random.randint(0, g_screen_width - g_babsoner_width),
                              0,
                              g_babsoner_vy,
                              True)
            self.babsoners.append(babson)
            print "Babsoner Created! - %d" % (len(self.babsoners))
        else:
            for babsoner in self.babsoners:
                if babsoner.is_visible == False:
                    babsoner.reset(random.randint(0, g_screen_width - g_babsoner_width), 0, g_babsoner_vy)
                    break

    def removeBabsoner(self, babsoner):
        babsoner.is_visible = 1

    def getScore(self, num_rmvd_babsoners, ellapsed_time):
        self.score = num_rmvd_babsoners
        return self.score

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

    def printAll(self):
        print "== Snowman =="
        print "width:", self.width
        print "height:", self.height
        print "x:", self.x
        print "y:", self.y
        print "vx:", self.vx
        print "lives:", self.lives
        print "============="

class Babsoner:
    """ Encodes state of babsoner """
    def __init__(self, width, height, x, y, vy, is_visible):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vy = vy
        self.is_visible = is_visible
        self.image = pygame.transform.scale(pygame.image.load("./babsoner.png"), (self.width, self.height))
        # Make image transparent
        alpha = 255
        self.image.fill((211, 242, 241, alpha), None, pygame.BLEND_RGBA_MULT)

    def reset(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.is_visible = True

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
        
        # Display score
        score = self.model.getScore(g_num_rmvd_babsoners, USEREVENT + 2)
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = g_screen_width/2
        screen.blit(text, textpos)
        
        # Displaying Snowman
        screen.blit(self.model.snowman.image, (model.snowman.x, model.snowman.y))

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
                #pygame.display.flip()  # commented to remove blinking


        pygame.display.flip()

############################################################################
# Controller Classes
############################################################################

class SnowManMouseController:
    """ """
    def __init__(self, model):
        self.model = model

    def handleMouseEvent(self, event):
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
            if babsoner.y > g_screen_height and babsoner.is_visible == True:
                babsoner.is_visible = False
                global g_num_rmvd_babsoners
                g_num_rmvd_babsoners += 1

    def create(self):
        """ """
        self.model.createBabsoner(g_babsoner_vy)

class SnowManCollisionController:
    """ """
    def __init__(self, model):
        self.model = model

    def check(self):
        """ Check collision between snowman and babsoner """
        # Rect(left, top, width, height) -> Rect
        # Rect((left, top), (width, height)) -> Rect
        rect_snowman = pygame.Rect(model.snowman.x, model.snowman.y, model.snowman.width, model.snowman.height)
        for babsoner in self.model.babsoners:
            if babsoner.is_visible == True:
                rect = pygame.Rect(babsoner.x, babsoner.y, babsoner.width, babsoner.height)
                if rect.colliderect(rect_snowman):
                    model.snowman.lives -= 1
                    babsoner.is_visible = False
                    print "Collision! - remaining lives: %d" % (model.snowman.lives)

############################################################################
# Add Music
############################################################################

def play_music(loop,start):
    pygame.mixer.music.play(loop,start)

def stop_music():
    pygame.mixer.music.stop()

############################################################################
# Main
############################################################################

if __name__ == "__main__":
    pygame.init()

    # Initialize screen
    size = (g_screen_width, g_screen_height)
    screen = pygame.display.set_mode(size)

    # MVC objects
    model = SnowManModel()
    view = SnowManView(model, screen)
    controller_mouse = SnowManMouseController(model)
    controller_babsoner = SnowManBabsonerController(model)
    controller_collision = SnowManCollisionController(model)

    # Create timer event for user event
    pygame.time.set_timer(USEREVENT + 1, 50)
    pygame.time.set_timer(USEREVENT + 2, 1000)

    #load music
    pygame.mixer.music.load('jamesbond.mp3')

    #set music volume
    pygame.mixer.music.set_volume(1.0) #value between 0.0 and 1.0

    # Running loop
    running = True
    play_music(-1,0.0)
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == MOUSEMOTION:
                controller_mouse.handleMouseEvent(event)

            if event.type == USEREVENT + 1:
                controller_babsoner.update()
                controller_collision.check()

            if event.type == USEREVENT + 2:
                controller_babsoner.create()

        view.draw()
        time.sleep(.001)
        if model.snowman.lives == 0:
            running = False
            # Add code for video here!

    pygame.quit()


