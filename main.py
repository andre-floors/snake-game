# SNAKE GAME
# This is an activity for Data Structures & Algorithms of BSIT 2-2. Developed by Andre Ryan F. Flores.
# This game uses the pygame library, which is used to make video games using the Python language.

# CODE BELOW IS THE BASE STARTING CODE FROM PYGAME, TO TEST THE GAME.

# initialize pygame
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("green")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()