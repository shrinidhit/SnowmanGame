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
    """Encodes overall game state of Snowman game"""
    def __init__(self):
        # initialize
        self.snowman = SnowMan(200,100,screen_height,screen_width/2.0-50,0) # set screen_width
        self.babsoner = []
        self.score = 0
    #def CreateSnowman(self, x, y)

#change to babsoner -- radius changes to width and height
#random -- height and width ratio stays same
# In controller calculate time it takes babsoner to reach bottom
# When reaches bottom call removebabsoner
# -> count number of times removebabsoner called -> num_babsoners -> score

    def CreateBabsoner(self):
            a = random.randint(50,150)
            babson = Babsoner(a,a*2,random.randint(a/2.0,screen_width-a/2.0),0,)
            self.babsoner.append(babson)
        
    def RemoveBabsoner(self, babsoner):
        


    def GetScore(self, , ellapsed_time):
        
        final_score = num_snow_balls + ellapsed_time
        return final_score
    
    def update(self):
        self.snowman.update()
        self.score.update()

class SnowMan:
    """ """
    def __init__(self):
        pass

class Babsoner:
    """ """
    def __init__(self):
        pass

class SnowManView:
    """ """
    def __init__(self):
        pass

    def draw(self):
        pass

class SnowManMouseController:
    """ """
    def __init__(self):
        pass

    def HandleMouseEvent(self):
        pass

class SnowManSnowBallController:
    """ """
    def __init__(self):
        pass

class SnowManCollisionController:
    """ """
    def __init__(self):
        pass