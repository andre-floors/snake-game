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

# grid and cell sizes
CELL_SIZE = 25
GRID_WIDTH = 30
GRID_HEIGHT = 26
GRID_TOP_LEFT_X = 0
GRID_TOP_LEFT_Y = 101

# base coordinates for snake and food
snake = Snake([(5, 10), (4, 10), (3, 10)])
food = Food(25, 25)

# score and font
score = 0
font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 60)

# high score
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

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
move_delay = 0.15
has_moved = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake.set_direction(event.key)
    
            # Move after WASD keys are pressed
            if event.key in (pygame.K_w, pygame.K_s, pygame.K_d):
                has_moved = True

    # Check for collision against boundaries
    if snake.is_collision() or snake.is_self_collision():
        print("Game Over: Collision detected")
        running = False

    # Change high score when surpassed
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

    # Movement speed of snake
    current_time = time.time()
    if has_moved and current_time - last_move_time > move_delay:
        snake.move(snake.direction)
        last_move_time = current_time

    # Check for food collision
    if snake.get_positions()[0] == food.position:
        if food.is_bonus:
            snake.grow(3)       # Grow by 3 for bonus food
            score += 3
        else:
            snake.grow(1)       # Regular growth
            score += 1
        food.respawn()


    # fill the screen with the background
    screen.blit(background, (0, 0))
    # fill the screen with the high score text
    high_score_font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 20)
    high_score_text = high_score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect(center=(110, 110))  # Positioned above the grid
    screen.blit(high_score_text, high_score_rect)
    # fill the screen with the scoreboard and the score counter
    screen.blit(scoreboard, (275, 5))

    # score text
    score_text = font.render(f"{score}", True, (0, 0, 0))
    text_rect = score_text.get_rect(center=(400, 60))  # Center on scoreboard
    screen.blit(score_text, text_rect)

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

        # Display food with animation
        animated_img, size = food.get_animated_image()
        x, y = grid_to_pixel(*food.position)
        x += (CELL_SIZE - size) // 2
        y += (CELL_SIZE - size) // 2
        screen.blit(animated_img, (x, y))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

# exit game
pygame.quit()