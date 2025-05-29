# SNAKE GAME
# This is an activity for Data Structures & Algorithms of BSIT 2-2. Developed by Andre Ryan F. Flores.
# This game uses the pygame library, which is used to make video games using the Python language.

# CODE BELOW IS THE BASE STARTING CODE FROM PYGAME, TO TEST THE GAME.

# IMPORT
import pygame
import time
from menu import Menu
from snake import Snake
from food import Food

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True

# SOUNDS
move_sound = pygame.mixer.Sound("assets/sfx/move.wav")
eat_food_sound = pygame.mixer.Sound("assets/sfx/food.wav")
eat_food_sound.set_volume(0.5)
eat_bonus_food_sound = pygame.mixer.Sound("assets/sfx/bonus-food.wav")
eat_bonus_food_sound.set_volume(0.5)
beat_highscore_sound = pygame.mixer.Sound("assets/sfx/beat-highscore.wav")
beat_highscore_sound.set_volume(0.5)
countdown_tick_sound = pygame.mixer.Sound("assets/sfx/countdown.wav")
countdown_tick_sound.set_volume(0.5)

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

# FUNCTIONS
# Computation for cell placement on grid
def grid_to_pixel(col, row):
    x = GRID_TOP_LEFT_X + col * CELL_SIZE
    y = GRID_TOP_LEFT_Y + row * CELL_SIZE
    return (x, y)

# Countdown upon resuming game
def start_countdown(seconds):
    global in_countdown, countdown_start_time, countdown_seconds
    in_countdown = True
    countdown_start_time = time.time()
    countdown_seconds = seconds
    last_tick_played = None

# import background
background = pygame.image.load("assets/playbackground_hard.png").convert()

# import scoreboard
scoreboard = pygame.image.load("assets/scoreboard.png").convert_alpha()
scoreboard.set_colorkey((255, 255, 255))  # Make white transparent
scoreboard = pygame.transform.scale(scoreboard, (250, 115))  # new width x height

last_move_time = time.time()
move_delay = 0.15 # Speed of the snake
has_moved = False # To ensure no movement until movement keys are pressed
paused = False # For the pause feature
in_countdown = False
countdown_start_time = 0
countdown_seconds = 3
remaining = countdown_seconds  # for countdown ticking
last_tick_played = None
high_score_surpassed = False

# Show menu before game
menu = Menu(screen)
menu.run()

# Fade in the game screen after menu fades out
fade_surface = pygame.Surface(screen.get_size())
fade_surface.fill((0, 0, 0))
fade_alpha = 255  # Start fully black
fade_speed = 5    # Speed of fade (alpha decrease per frame)

# Disable input during fade
fade_start_time = time.time()
disable_input_duration = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Disable key input for first second of fade-in
        if time.time() - fade_start_time < disable_input_duration:
            continue

        # Block all key inputs during countdown
        if in_countdown:
            continue

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if paused:
                    paused = False
                    start_countdown(3)
                else:
                    paused = True
            elif not paused:
                snake.set_direction(event.key)
                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN):
                    has_moved = True
                    move_sound.play()
    
    if not paused and not in_countdown:
        # Check for collision against boundaries
        if snake.is_collision() or snake.is_self_collision():
            print("Game Over: Collision detected")
            running = False

        # Change high score when surpassed
        if score > high_score:
            if not high_score_surpassed:
                beat_highscore_sound.play()
                high_score_surpassed = True
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
                eat_bonus_food_sound.play()
            else:
                snake.grow(1)       # Regular growth
                score += 1
                eat_food_sound.play()
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

    # Pause overlay
    if paused:
        pause_overlay = pygame.Surface((800, 800))
        pause_overlay.set_alpha(128)  # Semi-transparent
        pause_overlay.fill((0, 0, 0))  # Black overlay
        screen.blit(pause_overlay, (0, 0))

        pause_font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 50)
        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(400, 400))
        screen.blit(pause_text, pause_rect)

    if in_countdown:
        elapsed = time.time() - countdown_start_time
        new_remaining = countdown_seconds - int(elapsed)
        if new_remaining != remaining:
            remaining = new_remaining

        if remaining > 0:
            # For countdown sound
            if remaining != last_tick_played:
                countdown_tick_sound.play()
                last_tick_played = remaining
            
            # Draw black overlay
            overlay = pygame.Surface((800, 800))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Draw countdown number
            countdown_font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 100)
            countdown_text = countdown_font.render(str(remaining), True, (255, 255, 255))
            countdown_rect = countdown_text.get_rect(center=(400, 400))
            screen.blit(countdown_text, countdown_rect)
        else:
            in_countdown = False  # Countdown done

    # Fade into the screen
    if fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        fade_alpha -= fade_speed
        if fade_alpha < 0:
            fade_alpha = 0

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

# exit game
pygame.quit()