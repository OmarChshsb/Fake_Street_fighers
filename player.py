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
        self.x  = 0 

        if keys
    

    def attack(self)
    

    def jump(self)


    def guard(self)
        
    
    def take_damage(self, amount)
    

    def gravity(self)
    

    def update_state(self)
        







class Animation():

    def __init__(self, x, y, character_name, action, delay, scale = 3):
        self.x = x
        self.y = y
        self.action = action
        self.delay = delay
        self.character_name = character_name
        self.scale = scale
        self.frame_index = 0
        self.frame_timer = 0
        self.sprites = []
        
        folder_path = os.path.join("assets", "Characters", self.character_name, self.action)
        sprites_name = os.listdir(folder_path)

        for name in sprites_name:
            path = os.path.join(folder_path, name)
            image = pygame.image.load(path).convert_alpha()
            self.sprites.append(image)

    
    def update(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.delay:
            self.frame_index = (self.frame_index + 1) % len(self.sprites)
            self.frame_timer = 0


    def draw(self, window):
        sprite = self.sprites[self.frame_index]
        sprite = pygame.transform.scale(sprite, (sprite.get_width() , sprite.get_height() ))
        window.blit(sprite, (self.x, self.y))