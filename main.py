# SNAKE GAME
# This is an activity for Data Structures & Algorithms of BSIT 2-2. Developed by Andre Ryan F. Flores.
# This game uses the pygame library, which is used to make video games using the Python language.

# CODE BELOW IS THE BASE STARTING CODE FROM PYGAME, TO TEST THE GAME.

# initialize pygame
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True

# initialize important variables
CELL_SIZE = 25
GRID_WIDTH = 25
GRID_HEIGHT = 25  # Adjust to fit only the visible vertical area, or add padding if needed

GRID_TOP_LEFT_X = 0   # X offset (800 - 750) / 2 = 25
GRID_TOP_LEFT_Y = 101  # Padding from top to leave space for scoreboard

snake_positions = [(5, 10), (4, 10), (3, 10)]  # head, body, tail
food_position = (12, 18)

# functions
def grid_to_pixel(col, row):
    x = GRID_TOP_LEFT_X + col * CELL_SIZE
    y = GRID_TOP_LEFT_Y + row * CELL_SIZE
    return (x, y)

# background
background = pygame.image.load("assets/playbackground_hard.png").convert()
scoreboard = pygame.image.load("assets/scoreboard.png").convert_alpha()
scoreboard.set_colorkey((255, 255, 255))  # Make white transparent
scoreboard = pygame.transform.scale(scoreboard, (250, 115))  # new width x height

# import snake assets
snake_head = pygame.image.load("assets/snake_head.png").convert()
snake_head.set_colorkey((255, 255, 255))
snake_head = pygame.transform.scale(snake_head, (25, 25))

snake_body = pygame.image.load("assets/snake_body.png").convert()
snake_body.set_colorkey((255, 255, 255))
snake_body = pygame.transform.scale(snake_body, (25, 25))

snake_tail = pygame.image.load("assets/snake_tail.png").convert()
snake_tail.set_colorkey((255, 255, 255))
snake_tail = pygame.transform.scale(snake_tail, (25, 25))

# import and resize food
food = pygame.image.load("assets/food.png").convert_alpha()
food.set_colorkey((255, 255, 255))
food = pygame.transform.scale(food, (25, 25))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen the background
    screen.blit(background, (0, 0))
    screen.blit(scoreboard, (275, 5))

    for i, segment in enumerate(snake_positions):
        if i == 0:
            screen.blit(snake_head, grid_to_pixel(*segment))
        elif i == len(snake_positions) - 1:
            screen.blit(snake_tail, grid_to_pixel(*segment))
        else:
            screen.blit(snake_body, grid_to_pixel(*segment))

    screen.blit(food, grid_to_pixel(*food_position))


    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()