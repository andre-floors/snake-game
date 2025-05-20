# SNAKE GAME
# This is an activity for Data Structures & Algorithms of BSIT 2-2. Developed by Andre Ryan F. Flores.
# This game uses the pygame library, which is used to make video games using the Python language.

# CODE BELOW IS THE BASE STARTING CODE FROM PYGAME, TO TEST THE GAME.

# IMPORT
import pygame
import time
from snake import Snake
from food import Food

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

snake = Snake([(5, 10), (4, 10), (3, 10)])
food = Food(25, 25)

# functions
def grid_to_pixel(col, row):
    x = GRID_TOP_LEFT_X + col * CELL_SIZE
    y = GRID_TOP_LEFT_Y + row * CELL_SIZE
    return (x, y)

# import background
background = pygame.image.load("assets/playbackground_hard.png").convert()

# import scoreboard
scoreboard = pygame.image.load("assets/scoreboard.png").convert_alpha()
scoreboard.set_colorkey((255, 255, 255))  # Make white transparent
scoreboard = pygame.transform.scale(scoreboard, (250, 115))  # new width x height

last_move_time = time.time()
move_delay = 1
has_moved = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake.set_direction(event.key)
            has_moved = True  # Only start moving after a key is pressed


    current_time = time.time()
    if has_moved and current_time - last_move_time > move_delay:
        snake.move(snake.direction)
        last_move_time = current_time

    # fill the screen with the background
    screen.blit(background, (0, 0))
    # fill the screen with the scoreboard
    screen.blit(scoreboard, (275, 5))

    # SNAKE ORIENTATION
    if snake.direction == 'UP':
        head_img = snake.get_head_image(snake.direction)
    elif snake.direction == 'DOWN':
        head_img = snake.get_head_image(snake.direction)
    elif snake.direction == 'LEFT':
        head_img = snake.get_head_image(snake.direction)
    elif snake.direction == 'RIGHT':
        head_img = snake.get_head_image(snake.direction)

    positions = snake.get_positions()

    for i, segment in enumerate(positions):
        if i == 0:
            # HEAD
            head_img = snake.get_head_image(snake.direction)
            screen.blit(head_img, grid_to_pixel(*segment))
        elif i == len(positions) - 1:
            # TAIL
            prev_pos = positions[i - 1]
            tail_img = snake.get_tail_image(prev_pos, segment)
            screen.blit(tail_img, grid_to_pixel(*segment))
        else:
            # BODY
            prev_pos = positions[i - 1]
            next_pos = positions[i + 1]
            body_img = snake.get_body_image(prev_pos, segment, next_pos)
            screen.blit(body_img, grid_to_pixel(*segment))

        screen.blit(food.image, grid_to_pixel(*food.position))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

# exit game
pygame.quit()