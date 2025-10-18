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


class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, name):
        super().__init__()
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "Right"   # "Left" o "Right"
        self.current_state = "idle"
        self.name = name           # nome del personaggio
        self.speed = 7

        # Animazioni (usa la nuova classe)
        self.idle = Animation(x, y, name, "Idle", 40)
        self.run = Animation(x, y, name, "WalkForward", 100)

        self.image = self.idle.sprites[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hp = 100
        self.max_hp = 100

    def handle_input(self, keys, left_key, right_key):
        """Muove il player con i tasti passati (così possiamo usare set diversi per A/B)."""
        self.x_vel = 0

        if keys[left_key]:
            self.x_vel = -self.speed
            self.direction = "Left"
            self.current_state = "run"
        elif keys[right_key]:
            self.x_vel = self.speed
            self.direction = "Right"
            self.current_state = "run"
        else:
            self.current_state = "idle"

    def update(self, dt):
        """Aggiorna la posizione e la giusta animazione."""
        self.x += self.x_vel
        self.rect.x = self.x

        # Scegli animazione
        if self.current_state == "run":
            anim = self.run
        else:
            anim = self.idle

        anim.x = self.x
        anim.y = self.y
        anim.update(dt)

        # Se guarda a sinistra → flip
        current_sprite = anim.sprites[anim.frame_index]
        if self.direction == "Left":
            current_sprite = pygame.transform.flip(current_sprite, True, False)

        self.image = pygame.transform.scale(
            current_sprite,
            (current_sprite.get_width() * anim.scale, current_sprite.get_height() * anim.scale)
        )

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))





class Animation():

    def __init__(self, x, y, character_name, action, delay, scale = 1):
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




def get_background(window, background):
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        window.blit(background, (0, 0)) 


def main(window):
    clock = pygame.time.Clock()

    player1 = Player(400, 530, "Hitto")  # nome cartella in assets/Characters/
    player2 = Player(1200, 530, "Crash")

    run = True
    while run:
        dt = clock.tick(FPS)
        keys = pygame.key.get_pressed()

        # Player1: usa A/D
        player1.handle_input(keys, pygame.K_a, pygame.K_d)
        # Player2: usa frecce
        player2.handle_input(keys, pygame.K_LEFT, pygame.K_RIGHT)


        player1.update(dt)
        player2.update(dt)

        get_background(window, background)
        player1.draw(window)
        player2.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
