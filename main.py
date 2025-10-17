import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("Platform")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))

# gestione e caricamento sprite
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprites_sheets(dir1, dir2, frame_width, frame_height, direction=False):
    canvas_size = 96
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []

        num_frames = sprite_sheet.get_width() // canvas_size
        for i in range(num_frames):
            surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(
                i * canvas_size + (canvas_size - frame_width) // 2,
                (canvas_size - frame_height) // 2,
                frame_width, frame_height
            )
            surface.blit(sprite_sheet, (0, 0), rect)
            # Scale up the sprite to 3x size (288x288)
            scaled_surface = pygame.transform.scale(surface, (frame_width * 3, frame_height * 3))
            sprites.append(scaled_surface)

        key = image.replace(".png", "")
        if direction:
            all_sprites[key + "_right"] = sprites
            all_sprites[key + "_left"] = flip(sprites)
        else:
            all_sprites[key] = sprites

    return all_sprites

# classe Player
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITE = load_sprites_sheets("Knight", "knight", 96, 96, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITE[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))

# inizializza lo sfondo
def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

# disegna lo sfondo e il player
def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)
    player.draw(window)
    pygame.display.update()

# gestisci il movimento del player
def handle_move(player):
    keys = pygame.key.get_pressed()
    player.x_vel = 0

    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)

# loop principale
def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")
    player = Player(100, 150, 50, 50)
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player)
        draw(window, background, bg_image, player)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)