import pygame

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Activity")



bg_img = pygame.image.load("game_resources/Background.png").convert_alpha()
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

sprite_sheet_image = pygame.image.load('IDLE.png').convert_alpha()

BLACK = (0, 0, 0)

def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))

    return image

frame_0 = get_image(sprite_sheet_image, 32, 32, 3, BLACK)

run = True
while run:
     
     screen.blit(bg_img, (0, 0))

     screen.blit(frame_0, (0, 0))

     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
     pygame.display.update()

pygame.quit()