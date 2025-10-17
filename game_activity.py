import os
import random 
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Fake_Fighers")

WIDTH, HEIGHT= 1920, 1080
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
frame_index = 0
frame_timer = 0
frame_delay = 100

background  = pygame.image.load(join("assets", "Background", "Background.png"))



class Animation():

    def __init__(self, x, y, folder, delay):
        self.x = x
        self.y = y
        self.folder = folder
        self.delay = delay
        self.frame_index = 0
        self.frame_timer = 0
        self.sprites = []
        
        folder_path = os.path.join("assets", "Knight", "Hitto", folder)
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




def get_background(window, background):
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        window.blit(background, (0, 0)) 


def main(window):
    clock = pygame.time.Clock()

    anim = Animation(600, 530, "Idle", 80)

    run = True
    while run:
        dt = clock.tick(FPS)

        get_background(window, background)
        anim.update(dt)
        anim.draw(window)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    
        pygame.display.update()
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
