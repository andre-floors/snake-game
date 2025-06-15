# SNAKE GAME
# This is an activity for Data Structures & Algorithms of BSIT 2-2. Developed by Andre Ryan F. Flores.
# This game uses the pygame library, which is used to make video games using the Python language.

# Imports
import pygame
import time
import settings
from menu import Menu
from snake import Snake
from food import Food

# Setup Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
running = True

# Sounds
move_sound = pygame.mixer.Sound("assets/sfx/move.wav")
eat_food_sound = pygame.mixer.Sound("assets/sfx/food.wav")
eat_food_sound.set_volume(0.5)
eat_bonus_food_sound = pygame.mixer.Sound("assets/sfx/bonus-food.wav")
eat_bonus_food_sound.set_volume(0.5)
beat_highscore_sound = pygame.mixer.Sound("assets/sfx/beat-highscore.wav")
beat_highscore_sound.set_volume(0.5)
countdown_tick_sound = pygame.mixer.Sound("assets/sfx/countdown.wav")
countdown_tick_sound.set_volume(0.5)
game_over_sound = pygame.mixer.Sound("assets/sfx/game-over.wav")
game_over_sound.set_volume(0.5)

# Grid and Cell Sizes
CELL_SIZE = 25
GRID_WIDTH = 30
GRID_HEIGHT = 26
GRID_TOP_LEFT_X = 0
GRID_TOP_LEFT_Y = 101

# Load High Score
def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 

# Computation for cell placement on grid
def grid_to_pixel(col, row):
    x = GRID_TOP_LEFT_X + col * CELL_SIZE
    y = GRID_TOP_LEFT_Y + row * CELL_SIZE
    return (x, y)

# Countdown upon resuming game
def start_countdown(seconds):
    global in_countdown, countdown_start_time, countdown_seconds, last_tick_played
    in_countdown = True
    countdown_start_time = time.time()
    countdown_seconds = seconds
    last_tick_played = None

# Import play background image
background = pygame.image.load("assets/images/game/play-background.png").convert()

# Import scoreboard image
scoreboard = pygame.image.load("assets/images/game/scoreboard.png").convert_alpha()
scoreboard.set_colorkey((255, 255, 255))  # Make white transparent
scoreboard = pygame.transform.scale(scoreboard, (250, 115))  # new width x height

# Import pause button images
pause_resume = pygame.image.load("assets/images/game/pause-resume.png")
pause_resume_hover = pygame.image.load("assets/images/game/pause-resume-hover.png")
pause_audio_on = pygame.image.load("assets/images/game/pause-audioon.png")
pause_audio_on_hover = pygame.image.load("assets/images/game/pause-audioon-hover.png")
pause_audio_off = pygame.image.load("assets/images/game/pause-audiooff.png")
pause_audio_off_hover = pygame.image.load("assets/images/game/pause-audiooff-hover.png")
pause_exit = pygame.image.load("assets/images/game/pause-exit.png")
pause_exit_hover = pygame.image.load("assets/images/game/pause-exit-hover.png")

# Import game over images
gameover_retry = pygame.image.load("assets/images/game/gameover-retry.png")
gameover_retry_hover = pygame.image.load("assets/images/game/gameover-retry-hover.png")
gameover_exit = pygame.image.load("assets/images/game/gameover-exit.png")
gameover_exit_hover = pygame.image.load("assets/images/game/gameover-exit-hover.png")

# Resizing pause buttons
new_width = int(500 * 0.7)   # 350
new_height = int(100 * 0.7)  # 70
button_size = (new_width, new_height)
pause_buttons = {
    "resume": [pygame.transform.scale(pause_resume, button_size), pygame.transform.scale(pause_resume_hover, button_size)],
    "audio_on": [pygame.transform.scale(pause_audio_on, button_size), pygame.transform.scale(pause_audio_on_hover, button_size)],
    "audio_off": [pygame.transform.scale(pause_audio_off, button_size), pygame.transform.scale(pause_audio_off_hover, button_size)],
    "exit": [pygame.transform.scale(pause_exit, button_size), pygame.transform.scale(pause_exit_hover, button_size)]
}

pause_button_rects = {
    "resume": pause_buttons["resume"][0].get_rect(center=(400, 300)),
    "audio": pause_buttons["audio_on"][0].get_rect(center=(400, 370)),  # same rect for both on/off
    "exit": pause_buttons["exit"][0].get_rect(center=(400, 440))
}

# Show menu before game
menu = Menu(screen)
menu.run()

settings.load_settings()

# Volume Update
volume = settings.settings["volume"] / 100.0
move_sound.set_volume(volume)
eat_food_sound.set_volume(volume)
eat_bonus_food_sound.set_volume(volume)
beat_highscore_sound.set_volume(volume)
countdown_tick_sound.set_volume(volume)
game_over_sound.set_volume(volume)
# Game Speed Update
move_delay = settings.SPEED_VALUES[settings.settings["game_speed"]]
# High Score Update
high_score = load_high_score()
# Render Snake (if color was changed)
snake = Snake([(5, 10), (4, 10), (3, 10)])
# Cell range of food spawning
food = Food(30, 26, snake.get_positions())

# Game State Flags
score = 0
score_font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 80)
high_score_surpassed = False
game_over = False
game_over_alpha = 0
game_over_fade_speed = 5

# Audio Settings
audio_muted = False

# Movement Control
last_move_time = time.time()
has_moved = False

# Pause & Countdown
paused = False
in_countdown = False
countdown_start_time = 0
countdown_seconds = 3
remaining = countdown_seconds
last_tick_played = None

# Resize game over buttons
gameover_buttons = {
    "retry": [
        pygame.transform.scale(gameover_retry, button_size),
        pygame.transform.scale(gameover_retry_hover, button_size)
    ],
    "exit": [
        pygame.transform.scale(gameover_exit, button_size),
        pygame.transform.scale(gameover_exit_hover, button_size)
    ]
}

gameover_button_rects = {
    "retry": gameover_buttons["retry"][0].get_rect(center=(400, 350)),
    "exit": gameover_buttons["exit"][0].get_rect(center=(400, 420))
}

# Fade in the game screen after menu fades out
fade_surface = pygame.Surface(screen.get_size())
fade_surface.fill((0, 0, 0))
fade_alpha = 255
fade_speed = 5

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
            if event.key == pygame.K_ESCAPE and not game_over:
                if paused:
                    paused = False
                    start_countdown(3)
                else:
                    paused = True

                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            elif not paused and not game_over:
                snake.set_direction(event.key)
                if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN):
                    has_moved = True
                    move_sound.play()

        elif event.type == pygame.MOUSEBUTTONDOWN and paused:
            if pause_button_rects["resume"].collidepoint(event.pos):
                paused = False
                start_countdown(3)
            
            elif pause_button_rects["audio"].collidepoint(event.pos):
                audio_muted = not audio_muted
                move_sound.set_volume(0.0 if audio_muted else 1.0)
                eat_food_sound.set_volume(0.0 if audio_muted else 0.5)
                eat_bonus_food_sound.set_volume(0.0 if audio_muted else 0.5)
                beat_highscore_sound.set_volume(0.0 if audio_muted else 0.5)
                countdown_tick_sound.set_volume(0.0 if audio_muted else 0.5)
                game_over_sound.set_volume(0.0 if audio_muted else 0.5)

            elif pause_button_rects["exit"].collidepoint(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                fade_out(screen)
                menu.run()
                
                # Reset game state after returning from menu
                score = 0
                snake = Snake([(5, 10), (4, 10), (3, 10)])
                food = Food(30, 26, snake.get_positions())
                paused = False
                in_countdown = False
                has_moved = False
                high_score_surpassed = False
                last_move_time = time.time()

                # Fade in again after menu
                fade_alpha = 255
                fade_start_time = time.time()

                # Reload settings
                settings.load_settings()
                # Volume Update
                volume = settings.settings["volume"] / 100.0
                menu.music_channel.set_volume(volume)
                move_sound.set_volume(volume)
                eat_food_sound.set_volume(volume)
                eat_bonus_food_sound.set_volume(volume)
                beat_highscore_sound.set_volume(volume)
                countdown_tick_sound.set_volume(volume)
                game_over_sound.set_volume(volume)
                # Game Speed Update
                move_delay = settings.SPEED_VALUES[settings.settings["game_speed"]]
                # High Score Update
                high_score = load_high_score()

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if gameover_button_rects["retry"].collidepoint(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                fade_out(screen)

                # Reset game state to restart
                score = 0
                snake = Snake([(5, 10), (4, 10), (3, 10)])
                food = Food(30, 26, snake.get_positions())
                game_over = False
                game_over_alpha = 0
                paused = False
                in_countdown = False
                has_moved = False
                last_move_time = time.time()
                
                # Fade in again
                fade_alpha = 255
                fade_start_time = time.time()

            elif gameover_button_rects["exit"].collidepoint(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                fade_out(screen)
                menu.run()
                
                # Reset game state after returning from menu
                score = 0
                snake = Snake([(5, 10), (4, 10), (3, 10)])
                food = Food(30, 26, snake.get_positions())
                game_over = False
                game_over_alpha = 0
                paused = False
                in_countdown = False
                has_moved = False
                high_score_surpassed = False
                last_move_time = time.time()

                # Fade in again after menu
                fade_alpha = 255
                fade_start_time = time.time()

                # Reload settings
                settings.load_settings()
                # Volume Update
                volume = settings.settings["volume"] / 100.0
                menu.music_channel.set_volume(volume)
                move_sound.set_volume(volume)
                eat_food_sound.set_volume(volume)
                eat_bonus_food_sound.set_volume(volume)
                beat_highscore_sound.set_volume(volume)
                countdown_tick_sound.set_volume(volume)
                game_over_sound.set_volume(volume)
                # Game Speed Update
                move_delay = settings.SPEED_VALUES[settings.settings["game_speed"]]
                # High Score Update
                high_score = load_high_score()
                
    if not paused and not in_countdown and not game_over:
        # Check for collision against boundaries
        if snake.is_collision() or snake.is_self_collision():
            game_over_sound.play()
            game_over = True

        # Movement speed of snake
        current_time = time.time()
        if has_moved and current_time - last_move_time > move_delay:
            snake.move(snake.next_direction)
            snake.direction = snake.next_direction
            last_move_time = current_time

        # Check for food collision
        if snake.get_positions()[0] == food.position:
            if food.is_bonus:
                snake.grow(3) # Grow by 3 if it eats bonus food
                score += 3
                eat_bonus_food_sound.play()
            else:
                snake.grow(1)
                score += 1
                eat_food_sound.play()
            food.respawn(snake.get_positions())
        
        # Change high score and play sound when high score is surpassed
        if score > high_score:
            if not high_score_surpassed:
                beat_highscore_sound.play()
                high_score_surpassed = True
            high_score = score
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))

    # Render Background
    screen.blit(background, (0, 0))
    
    # Render High Score
    high_score_font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 30)
    high_score_icon = pygame.image.load("assets/images/game/high-score.png")
    high_score_icon = pygame.transform.scale(high_score_icon, (30, 30))
    high_score_text = high_score_font.render(f"{high_score}", True, (255, 255, 255))
    screen.blit(high_score_icon, (30, 90))
    screen.blit(high_score_text, (68, 89))

    # Render Scoreboard and Score
    screen.blit(scoreboard, (275, 5))
    score_text = score_font.render(f"{score}", True, (0, 0, 0))
    text_rect = score_text.get_rect(center=(400, 60))  # Center on scoreboard
    screen.blit(score_text, text_rect)

    # Orientation of Snake Head
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
            # Head
            head_img = snake.get_head_image(snake.direction)
            screen.blit(head_img, grid_to_pixel(*segment))
        elif i == len(positions) - 1:
            # Tail
            prev_pos = positions[i - 1]
            tail_img = snake.get_tail_image(prev_pos, segment)
            screen.blit(tail_img, grid_to_pixel(*segment))
        else:
            # Body
            prev_pos = positions[i - 1]
            next_pos = positions[i + 1]
            body_img = snake.get_body_image(prev_pos, segment, next_pos)
            screen.blit(body_img, grid_to_pixel(*segment))

    # Render food
    animated_img, size = food.get_animated_image()
    x, y = grid_to_pixel(*food.position)
    x += (CELL_SIZE - size) // 2
    y += (CELL_SIZE - size) // 2
    screen.blit(animated_img, (x, y))

    # Pause overlay
    if paused:
        pause_overlay = pygame.Surface((800, 800))
        pause_overlay.set_alpha(128)
        pause_overlay.fill((0, 0, 0))
        screen.blit(pause_overlay, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        resume_hovered = pause_button_rects["resume"].collidepoint(mouse_pos)
        screen.blit(pause_buttons["resume"][1 if resume_hovered else 0], pause_button_rects["resume"])

        audio_key = "audio_off" if audio_muted else "audio_on"
        audio_hovered = pause_button_rects["audio"].collidepoint(mouse_pos)
        screen.blit(pause_buttons[audio_key][1 if audio_hovered else 0], pause_button_rects["audio"])

        exit_hovered = pause_button_rects["exit"].collidepoint(mouse_pos)
        screen.blit(pause_buttons["exit"][1 if exit_hovered else 0], pause_button_rects["exit"])

        mouse_pos = pygame.mouse.get_pos()
        hovering = False

        for key, rect in pause_button_rects.items():
            if rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                hovering = True
                break

        if not hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Countdown overlay
    if in_countdown:
        elapsed = time.time() - countdown_start_time
        new_remaining = countdown_seconds - int(elapsed)
        if new_remaining != remaining:
            remaining = new_remaining

        if remaining > 0:
            if remaining != last_tick_played:
                countdown_tick_sound.play()
                last_tick_played = remaining
            
            overlay = pygame.Surface((800, 800))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            countdown_font = pygame.font.Font("assets/fonts/VCR_OSD_MONO_1.001.ttf", 100)
            countdown_text = countdown_font.render(str(remaining), True, (255, 255, 255))
            countdown_rect = countdown_text.get_rect(center=(400, 400))
            screen.blit(countdown_text, countdown_rect)
        else:
            in_countdown = False  # Countdown done

    # Game Over overlay
    if game_over:
        if game_over_alpha < 150:
            game_over_alpha += game_over_fade_speed
            if game_over_alpha > 150:
                game_over_alpha = 150

        red_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        red_overlay.fill((255, 0, 0, game_over_alpha))
        screen.blit(red_overlay, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        retry_hovered = gameover_button_rects["retry"].collidepoint(mouse_pos)
        screen.blit(gameover_buttons["retry"][1 if retry_hovered else 0], gameover_button_rects["retry"])

        exit_hovered = gameover_button_rects["exit"].collidepoint(mouse_pos)
        screen.blit(gameover_buttons["exit"][1 if exit_hovered else 0], gameover_button_rects["exit"])

        mouse_pos = pygame.mouse.get_pos()
        hovering = False

        for key, rect in gameover_button_rects.items():
            if rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                hovering = True
                break

        if not hovering:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Fade out when returning to main menu
    def fade_out(surface, speed=3):
        fade_surface = pygame.Surface(surface.get_size())
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 256, speed):
            fade_surface.set_alpha(alpha)
            surface.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(10)

    # Fade game into the screen when entering
    if fade_alpha > 0:
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        fade_alpha -= fade_speed
        if fade_alpha < 0:
            fade_alpha = 0

    pygame.display.flip()

    clock.tick(60)

# Exit Game
pygame.quit()