import os
import random 
import math
import pygame
from os import listdir
from os.path import isfile, join

from game_activity import Animation



class  Player(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y):
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "Right"
        self.idle = Animation(x, y, "Idle", 50)
        self.run = Animation(x, y, "Run", 50)
        first_sprite = self.idle.sprites[0]
        self.rect = first_sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def handle_input():
    

    def attack()
    

    def jump()


    def guard()
    

    def damage()
        
    
    def hp()
        
    
    def get_hitbox()
    

    def gravity()
    

    def update_state()