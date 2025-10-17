import pygame
import button

pygame.init()

#create window

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#font
font = pygame.font.SysFont("arialblack", 40)


#load images  
start_img = pygame.image.load('menu_resources/start_btn.png').convert_alpha()
exit_img = pygame.image.load('menu_resources/exit_btn.png').convert_alpha()

#create button istances
start_button =  button.Button(100, 200, start_img)
exit_button = button.Button(450, 200, exit_img)

#game loop 
run = True

while run:

    screen.fill((52, 78, 91))

    if start_button.draw(screen):
        print("Start")
    if exit_button.draw(screen):
        run = False

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
    

    pygame.display.update()

pygame.quit()  





