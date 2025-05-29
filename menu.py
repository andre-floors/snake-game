import pygame
import sys
import math
import time

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Load music
        self.menu_music = pygame.mixer.Sound("assets/sfx/menu-music.wav")
        self.menu_music.set_volume(0.5)
        self.music_channel = pygame.mixer.Channel(1)
        self.music_channel.play(self.menu_music, loops=-1)  # Loop forever

        # Load assets
        self.bg_image = pygame.image.load("assets/menu_background.png").convert()
        self.logo = pygame.image.load("assets/snake_game_logo.png").convert_alpha()
        self.button_play = pygame.image.load("assets/button-play.png").convert_alpha()
        self.button_settings = pygame.image.load("assets/button-settings.png").convert_alpha()
        self.button_customize = pygame.image.load("assets/button-customize.png").convert_alpha()
        self.button_credits = pygame.image.load("assets/button-credits.png").convert_alpha()
        self.button_exit = pygame.image.load("assets/button-exit.png").convert_alpha()

        # Resize assets
        self.logo = pygame.transform.scale(self.logo, (500, 250))
        self.buttons = [
            ("play", pygame.transform.scale(self.button_play, (250, 100))),
            ("settings", pygame.transform.scale(self.button_settings, (250, 100))),
            ("customize", pygame.transform.scale(self.button_customize, (250, 100))),
            ("credits", pygame.transform.scale(self.button_credits, (250, 100))),
            ("exit", pygame.transform.scale(self.button_exit, (250, 100)))
        ]

        # Background scrolling
        self.bg_offset_x = 0
        self.bg_offset_y = 0
        self.bg_scroll_speed = 0.5

        self.running = True

        # Calculate button positions
        screen_width, screen_height = self.screen.get_size()

        # Position the logo higher (e.g., 100 px from top)
        logo_y = 30
        self.logo_rect = self.logo.get_rect(center=(screen_width // 2, logo_y + self.logo.get_height() // 2))

        # Position buttons starting further down (e.g., 300 px)
        start_y = logo_y + self.logo.get_height()
        gap = -10 # space between buttons

        # Logo movement
        self.start_time = time.time()
        self.logo_base_y = logo_y + self.logo.get_height() // 2  # for bounce baseline

        self.button_rects = []
        for i, (_, button) in enumerate(self.buttons):
            y = start_y + i * (button.get_height() + gap)
            rect = button.get_rect(center=(screen_width // 2, y + button.get_height() // 2))
            self.button_rects.append(rect)

    def update_background(self):
        self.bg_offset_x = (self.bg_offset_x + self.bg_scroll_speed) % self.bg_image.get_width()
        self.bg_offset_y = (self.bg_offset_y + self.bg_scroll_speed) % self.bg_image.get_height()

        for x in range(-self.bg_image.get_width(), self.screen.get_width(), self.bg_image.get_width()):
            for y in range(-self.bg_image.get_height(), self.screen.get_height(), self.bg_image.get_height()):
                self.screen.blit(self.bg_image, (x + self.bg_offset_x, y + self.bg_offset_y))

    def draw_menu(self):
        # Bounce animation
        elapsed = time.time() - self.start_time
        bounce_offset = math.sin(elapsed * 2) * 5  # speed = 2, amplitude = 10px

        logo_rect = self.logo.get_rect(center=(self.screen.get_width() // 2, self.logo_base_y + bounce_offset))
        self.screen.blit(self.logo, logo_rect)

        for (_, button_img), rect in zip(self.buttons, self.button_rects):
            self.screen.blit(button_img, rect)

    def update_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        pointer = False
        for (name, button_img), rect in zip(self.buttons, self.button_rects):
            if self.is_click_on_image(button_img, rect, mouse_pos):
                pointer = True
                break

        if pointer:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def is_click_on_image(self, button_img, button_rect, mouse_pos):
        # Check if mouse is inside the button rect
        if button_rect.collidepoint(mouse_pos):
            # Convert global mouse position to relative position inside the image
            rel_x = mouse_pos[0] - button_rect.left
            rel_y = mouse_pos[1] - button_rect.top

            # Get pixel's alpha value at relative position
            pixel_alpha = button_img.get_at((rel_x, rel_y)).a
            if pixel_alpha > 0:  # pixel is not transparent
                return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_click_on_image(self.buttons[0][1], self.button_rects[0], event.pos):  # Play button
                    return 'play'
                elif self.is_click_on_image(self.buttons[-1][1], self.button_rects[-1], event.pos):  # Exit button
                    pygame.quit()
                    sys.exit()

        return None

    def fade_out(self, speed=10):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 256, speed):
            fade_surface.set_alpha(alpha)
            self.update_background()
            self.draw_menu()
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def fade_in(self, speed=10):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))
        for alpha in range(255, -1, -speed):
            fade_surface.set_alpha(alpha)
            self.screen.fill((0, 0, 0))  # Optional: clear screen before drawing
            self.update_background()
            self.draw_menu()
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

    # Inside Menu class
    def fade_out_music(self, duration_ms=1000):
        self.music_channel.fadeout(duration_ms)

    def run(self):
        while self.running:
            action = self.handle_events()
            if action == 'play':
                self.fade_out_music(1000)  # 1 second fade
                self.fade_out()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset cursor before exit
                return

            self.update_cursor()
            self.update_background()
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)