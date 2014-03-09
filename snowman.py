# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 20:18:57 2014

@author:
    SeongHyeok Im
    Shrinidhi Thirumalai
    Inseong Joe
"""

import pygame
from pygame.locals import *
import random
import math
import time

class SnowManModel:
    """ """
    def __init__(self):
        # initialize
        pass
    def CreateSnowman(self, x, y):
        pass

    def CreateBabsoner(self, radius, x, y):
        pass

    def RemoveBabsoner(self, Babsoner):
        pass

    def GetScore(self, num_babsoners, ellapsed_time):
        pass

class SnowMan:
    """Encodes state of snowman"""
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
    def __init__(self, width, height, x, y, color, vy, is_visible):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.vy = vy
        self.is_visible = is_visible

class SnowManView:
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self, model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        #Filling Background Color
        self.screen.fill(pygame.Color(211,242,241))
        #Displaying Babsoners
        for babsoner in self.model.babsoners:
            if babsoner.is_visible == 0:
                image = pygame.image.load("babsoner.png")
                pygame.transform.scale(image, (babsoner.width,babsoner.height)) #scales image to height and width
                image.rect = self.image.get_rect() #gets x and y coordinates of image
                image.rect.x = image.x #moves image to x and y location input:
                image.rect.y = image.y
                screen.blit(image, imagerect)
                pygame.display.flip()
        #Displaying Snowman
        snowman_image = pygame.image.load("snowman.png")
        pygame.transform.scale(image, (self.snowman.width,self.snowman.height)) #scales image to height and width
        snowman_image.rect = self.snowman_image.get_rect() #gets x and y coordinates of image
        snowman_image.rect.x = image.x #moves image to x and y location input:
        snowman_image.rect.y = image.y
        screen.blit(snowman_image, snowman_imagerect)
        pygame.display.flip()
        
class SnowManMouseController:
    """ """
    def __init__(self):
        pass

    def HandleMouseEvent(self):
        pass

class SnowManBabsonerController:
    """ """
    def __init__(self):
        pass

class SnowManCollisionController:
    """ """
    def __init__(self):
        pass