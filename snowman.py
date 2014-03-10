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
g_snowman_vx = 0
g_snowman_lives = 5

g_babsoner_width = 70
g_babsoner_height = 50
g_babsoner_vy = 10

g_max_babsoner = 10
g_num_rmvd_babsoners = 0
g_time = 0
g_level = 1

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
                               g_snowman_vx,
                               g_snowman_lives)
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
                    width = g_snowman_width
                    height = g_snowman_height
                    if g_level >= 3:
                        r = random.randint(80, 100 + g_level * 2)
                        if r > 100:
                            width *= float(r / 100)
                            height *= float(r / 100)
                    babsoner.reset(width,
                                   height,
                                   random.randint(0, g_screen_width - g_babsoner_width),
                                   0,
                                   g_babsoner_vy)
                    break

    def getScore(self, num_rmvd_babsoners):
        return self.score

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

    def reset(self, width, height, x, y, vy):
        self.width = width
        self.height = height
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

        # Display current information: lives, level and score
        font = pygame.font.Font(None, 36)
        text = font.render("Lives: %d / Level: %d / Score: %d" % (model.snowman.lives, g_level, self.model.score), \
                           1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = g_screen_width / 2
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
        pygame.display.flip()

    def playMovie(self):
        FPS = 60
        clock = pygame.time.Clock()
        movie = pygame.movie.Movie('real_wreckingball.mpg')
        movie.skip(41.5)
        screen = pygame.display.set_mode(movie.get_size())
        movie_screen = pygame.Surface(movie.get_size()).convert()
        movie.set_display(movie_screen)
        movie.play()
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    movie.stop()
                    playing = False
            screen.blit(movie_screen,(0,0))
            pygame.display.update()
            clock.tick(FPS)
            
class SnowManPreview:
    """ Pre-game sequence """
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        # Filling Background Color
        self.screen.fill(pygame.Color(211, 242, 241))

        # Display title
        font = pygame.font.Font(None, 40)
        title = font.render("Mission: Defend the Olin Snowman", 1, (10, 10, 10))
        textpos = title.get_rect()
        textpos.centerx = g_screen_width/2
        textpos.centery = g_screen_height/3
        screen.blit(title, textpos)

        # Display subtitle
        font = pygame.font.Font(None, 20)
        subtitle = font.render("Instructions: Use your mouse to dodge the babson beavers. Keep the Olin Snowman Alive", 1, (10, 10, 10))
        subtextpos = subtitle.get_rect()
        subtextpos.centerx = g_screen_width/2
        subtextpos.centery = g_screen_height/2
        screen.blit(subtitle, subtextpos)

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
                global g_num_rmvd_babsoners
                g_num_rmvd_babsoners += 1
                babsoner.is_visible = False
                self.model.score += g_level

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

def playMusic(loop,start):
    pygame.mixer.music.play(loop,start)

def stopMusic():
    pygame.mixer.music.stop()
    
def pauseMusic():
    pygame.mixer.music.pause()

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
    preview = SnowManPreview(model, screen)
    controller_mouse = SnowManMouseController(model)
    controller_babsoner = SnowManBabsonerController(model)
    controller_collision = SnowManCollisionController(model)

    # Create timer event for preview
    pygame.time.set_timer(USEREVENT + 1, 1000)
    while g_time < 5:
        for event in pygame.event.get():
            if event.type == QUIT:
                exitGame()
                sys.exit(0)

            if event.type == USEREVENT + 1:
                g_time += 1
        preview.draw()

    # Create timer event for user event
    pygame.time.set_timer(USEREVENT + 1, 50)
    pygame.time.set_timer(USEREVENT + 2, 800)
    pygame.time.set_timer(USEREVENT + 3, 8000)    # every 8 seconds

    #load music
    pygame.mixer.music.load('jamesbond.mp3')

    # set music volume
    pygame.mixer.music.set_volume(1.0) #value between 0.0 and 1.0

    #load video
    #movie = pygame.movie.Movie('real_wreckingball.mpg')

    # Running loop
    running = True
    playMusic(-1,0.0)
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

            if event.type == USEREVENT + 3:
                g_babsoner_vy += 2
                g_level += 1
                print "Speed UP!"
                if g_level % 10 == 1:
                    stopMusic()
                    pygame.mixer.music.load('jamesbond.mp3')
                    playMusic(-1,0.0)
                    jamestime = pygame.mixer.music.get_pos()
                if g_level % 10 == 6:
                    stopMusic()
                    pygame.mixer.music.load('pinkpanther.mp3')
                    playMusic(-1,0.0)
                    panthertime = pygame.mixer.music.get_pos()
                if g_level % 10 == range(2,6):
                    pygame.mixer.music.load('jamesbond.mp3')
                    pygame.mixer.music.set_pos(jamestime)
                    playMusic(-1,jamestime)
                    newtime = pygame.mixer.music.get_pos()
                    jamestime += newtime
                if g_level % 10 == range(6,11):
                    pygame.mixer.music.load('pinkpanther.mp3')
                    pygame.mixer.music.set_pos(panthertime)
                    playMusic(-1,panthertime)
                    newwtime = pygame.mixer.music.get_pos()
                    panthertime += newwtime
                    
                    
                    

        view.draw()
        time.sleep(.001)

        if model.snowman.lives <= 0:
            running = False
            # Add code for video here!
            pygame.mixer.quit()
    #Printing score:

    #Playing wrecking ball movie:
    view.playMovie()
    #Ending Game:
    pygame.quit()
