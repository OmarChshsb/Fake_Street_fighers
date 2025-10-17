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
        super().__init__()
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "Right"
        self.current_state = "idle"
        self.idle = Animation(x, y, "Idle", 50)
        self.run = Animation(x, y, "Run", 50)
        first_sprite = self.idle.sprites[0]
        sprite = pygame.transform.scale(sprite, (sprite.get_width() , sprite.get_height() ))
        self.rect = first_sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp  = 100
        self.max_hp = 100

    def handle_input(self, keys):
    

    def attack(self)
    

    def jump(self)


    def guard(self)
        
    
    def take_damage(self, amount)
    

    def gravity(self)
    

    def update_state(self)