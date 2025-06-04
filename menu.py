# This file houses the entirety of the game's main menu

import pygame
import sys
import math
import time
import settings

class Menu:
    def __init__(self, screen):
        # Reload settings from settings.json every time menu is created
        settings.load_settings()

        self.screen = screen
        self.clock = pygame.time.Clock()

        # Important flags for game
        self.in_settings = False  # Tracks whether the settings menu is opened
        self.in_customize = False
        self.in_credits = False
        self.music_on = settings.settings["music_on"]
        self.volume = settings.settings["volume"]
        self.speed_states = list(settings.SPEED_VALUES.keys())
        self.current_speed_index = self.speed_states.index(settings.settings["game_speed"])
        self.selected_snake_color = settings.settings["snake_color"]

        # Prevent double clicking in settings
        self.settings_open_time = 0
        self.settings_click_lockout_duration = 0.1

        # Prevent double clicking in credits
        self.credits_open_time = 0
        self.credits_click_lockout_duration = 0.1

        # Load music
        self.menu_music = pygame.mixer.Sound("assets/sfx/menu-music.wav")
        self.music_channel = pygame.mixer.Channel(1)

        # Load assets
        self.bg_image = pygame.image.load("assets/images/menu/menu-background.png").convert()
        self.logo = pygame.image.load("assets/images/menu/snake-game-logo.png").convert_alpha()

        # Load buttons (both normal and hovered)
        self.hovered_button = None
        self.button_images = {
            "play": (
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-play.png").convert_alpha(), (250, 100)),
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-play-hover.png").convert_alpha(), (250, 100))
            ),
            "settings": (
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-settings.png").convert_alpha(), (250, 100)),
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-settings-hover.png").convert_alpha(), (250, 100))
            ),
            "customize": (
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-customize.png").convert_alpha(), (250, 100)),
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-customize-hover.png").convert_alpha(), (250, 100))
            ),
            "credits": (
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-credits.png").convert_alpha(), (250, 100)),
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-credits-hover.png").convert_alpha(), (250, 100))
            ),
            "exit": (
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-exit.png").convert_alpha(), (250, 100)),
                pygame.transform.scale(pygame.image.load("assets/images/menu/button-exit-hover.png").convert_alpha(), (250, 100))
            )
        }

        # Resize logo and buttons
        self.logo = pygame.transform.scale(self.logo, (500, 250))
        self.buttons = [(name, self.button_images[name][0]) for name in self.button_images]

        # Import settings elements
        self.hovered_settings_button = None
        self.settings_ui = pygame.image.load("assets/images/menu/settings-ui.png").convert_alpha()

        self.music_toggle_rect = pygame.Rect(0, 0, 0, 0)  # Placeholder to prevent attribute error

        self.volume_controls = {
            "down": pygame.image.load("assets/images/menu/volume-down.png").convert_alpha(),
            "up": pygame.image.load("assets/images/menu/volume-up.png").convert_alpha(),
            "toggle_on": pygame.image.load("assets/images/menu/music-on.png").convert_alpha(),
            "toggle_off": pygame.image.load("assets/images/menu/music-off.png").convert_alpha()
        }

        self.volume_down_rect = self.volume_controls["down"].get_rect(topleft=(368, 308))
        self.volume_up_rect = self.volume_controls["up"].get_rect(topleft=(552, 308))

        self.volume_levels = {
            0: pygame.image.load("assets/images/menu/volume-level-0.png").convert_alpha(),
            10: pygame.image.load("assets/images/menu/volume-level-10.png").convert_alpha(),
            20: pygame.image.load("assets/images/menu/volume-level-20.png").convert_alpha(),
            30: pygame.image.load("assets/images/menu/volume-level-30.png").convert_alpha(),
            40: pygame.image.load("assets/images/menu/volume-level-40.png").convert_alpha(),
            50: pygame.image.load("assets/images/menu/volume-level-50.png").convert_alpha(),
            60: pygame.image.load("assets/images/menu/volume-level-60.png").convert_alpha(),
            70: pygame.image.load("assets/images/menu/volume-level-70.png").convert_alpha(),
            80: pygame.image.load("assets/images/menu/volume-level-80.png").convert_alpha(),
            90: pygame.image.load("assets/images/menu/volume-level-90.png").convert_alpha(),
            100: pygame.image.load("assets/images/menu/volume-level-100.png").convert_alpha()
        }

        self.game_speeds = {
            "slow": (
                pygame.image.load("assets/images/menu/speed-slow.png").convert_alpha(),
                pygame.image.load("assets/images/menu/speed-slow-hover.png").convert_alpha()
            ),
            "normal": (
                pygame.image.load("assets/images/menu/speed-normal.png").convert_alpha(),
                pygame.image.load("assets/images/menu/speed-normal-hover.png").convert_alpha()
            ),
            "fast": (
                pygame.image.load("assets/images/menu/speed-fast.png").convert_alpha(),
                pygame.image.load("assets/images/menu/speed-fast-hover.png").convert_alpha()
            )
        }

        self.speed_rect = self.game_speeds["normal"][0].get_rect(topleft=(443, 376))

        self.reset_high_score = (
            pygame.image.load("assets/images/menu/reset-high-score.png").convert_alpha(),
            pygame.image.load("assets/images/menu/reset-high-score-hover.png").convert_alpha()
        )

        self.reset_rect = self.reset_high_score[0].get_rect(topleft=(252, 479))

        self.back_button = (
            pygame.image.load("assets/images/menu/back.png").convert_alpha(),
            pygame.image.load("assets/images/menu/back-hover.png").convert_alpha()
        )

        self.back_rect = self.back_button[0].get_rect(topleft=(351, 589))

        # Import customize elements
        self.customize_ui = pygame.image.load("assets/images/menu/customize-ui.png").convert_alpha()

        self.snake_color_selectors = {
            "white": pygame.image.load("assets/images/menu/snake-color-white.png").convert_alpha(),
            "red": pygame.image.load("assets/images/menu/snake-color-red.png").convert_alpha(),
            "orange": pygame.image.load("assets/images/menu/snake-color-orange.png").convert_alpha(),
            "yellow": pygame.image.load("assets/images/menu/snake-color-yellow.png").convert_alpha(),
            "green": pygame.image.load("assets/images/menu/snake-color-green.png").convert_alpha(),
            "blue": pygame.image.load("assets/images/menu/snake-color-blue.png").convert_alpha(),
            "violet": pygame.image.load("assets/images/menu/snake-color-violet.png").convert_alpha(),
            "black": pygame.image.load("assets/images/menu/snake-color-black.png").convert_alpha(),
        }

        self.snake_color_demo = {
            "white": pygame.image.load("assets/images/menu/demo-snake-white.png").convert_alpha(),
            "red": pygame.image.load("assets/images/menu/demo-snake-red.png").convert_alpha(),
            "orange": pygame.image.load("assets/images/menu/demo-snake-orange.png").convert_alpha(),
            "yellow": pygame.image.load("assets/images/menu/demo-snake-yellow.png").convert_alpha(),
            "green": pygame.image.load("assets/images/menu/demo-snake-green.png").convert_alpha(),
            "blue": pygame.image.load("assets/images/menu/demo-snake-blue.png").convert_alpha(),
            "violet": pygame.image.load("assets/images/menu/demo-snake-violet.png").convert_alpha(),
            "black": pygame.image.load("assets/images/menu/demo-snake-black.png").convert_alpha(),
        }

        self.snake_color_selected = pygame.image.load("assets/images/menu/snake-color-selected.png")

        self.snake_color_selector_coords = {
            "white": (245, 299),
            "red": (284, 299),
            "orange": (323, 299),
            "yellow": (362, 299),
            "green": (400, 299),
            "blue": (439, 299),
            "violet": (478, 299),
            "black": (517, 299)
        }

        # Import credits window
        self.hovered_credits_button = None
        self.credits_ui = pygame.image.load("assets/images/menu/credits-ui.png").convert_alpha()

        # Import credits label
        self.credit_label = pygame.image.load("assets/images/menu/credit-label.png").convert_alpha()

        # Background scrolling (for moving background)
        self.bg_offset_x = 0
        self.bg_offset_y = 0
        self.bg_scroll_speed = 0.5

        # Checks if menu is running
        self.running = True

        # Calculate button positions
        screen_width, screen_height = self.screen.get_size()

        # Position the logo higher
        logo_y = 30
        self.logo_rect = self.logo.get_rect(center=(screen_width // 2, logo_y + self.logo.get_height() // 2))

        # Position buttons from top to bottom
        start_y = logo_y + self.logo.get_height()
        gap = -10 # Vertical space between buttons

        # Logo movement (using sine wave)
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
        # Bounce animation (using sine wave)
        elapsed = time.time() - self.start_time
        bounce_offset = math.sin(elapsed * 2) * 5

        # Render menu buttons
        logo_rect = self.logo.get_rect(center=(self.screen.get_width() // 2, self.logo_base_y + bounce_offset))
        self.screen.blit(self.logo, logo_rect)

        for (name, _), rect in zip(self.buttons, self.button_rects):
            if name == self.hovered_button:
                img = self.button_images[name][1]  # hover version
            else:
                img = self.button_images[name][0]  # normal version
            self.screen.blit(img, rect)

        self.screen.blit(self.credit_label, (575, 783))

    def draw_settings(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Render Settings UI and buttons
        self.screen.blit(self.settings_ui, (0, 0))

        toggle_img = self.volume_controls["toggle_on"] if self.music_on else self.volume_controls["toggle_off"]
        self.music_toggle_rect = toggle_img.get_rect(topleft=(351, 256))
        self.screen.blit(toggle_img, self.music_toggle_rect)

        down_img = self.volume_controls["down"]
        up_img = self.volume_controls["up"]
        self.screen.blit(down_img, self.volume_down_rect)
        self.screen.blit(up_img, self.volume_up_rect)

        volume_key = int(round(self.volume / 10.0) * 10)
        volume_key = max(0, min(100, volume_key))
        self.screen.blit(self.volume_levels[volume_key], (398, 313))

        speed_key = self.speed_states[self.current_speed_index]
        speed_img = self.game_speeds[speed_key][1] if self.hovered_settings_button == "speed" else self.game_speeds[speed_key][0]
        self.screen.blit(speed_img, (443, 376))

        reset_img = self.reset_high_score[1] if self.hovered_settings_button == "reset" else self.reset_high_score[0]
        self.screen.blit(reset_img, self.reset_rect)

        back_img = self.back_button[1] if self.hovered_settings_button == "back" else self.back_button[0]
        self.screen.blit(back_img, self.back_rect)

    def draw_customize(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Render Customize UI and buttons
        self.screen.blit(self.customize_ui, (0, 0))

        for color, img in self.snake_color_selectors.items():
            selector_pos = self.snake_color_selector_coords[color]
            self.screen.blit(img, selector_pos)

            if self.selected_snake_color == color:
                highlight_pos = (selector_pos[0], selector_pos[1] - 3)
                selected_rect = self.snake_color_selected.get_rect(topleft=highlight_pos)
                self.screen.blit(self.snake_color_selected, selected_rect)

        demo_img = self.snake_color_demo.get(self.selected_snake_color)
        if demo_img:
            self.screen.blit(demo_img, (339, 360))

        back_img = self.back_button[1] if self.hovered_customize_button == "back" else self.back_button[0]
        self.screen.blit(back_img, self.back_rect)

    def draw_credits(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Render Credits UI and back button
        self.screen.blit(self.credits_ui, (0, 0))

        back_img = self.back_button[1] if self.hovered_credits_button == "back" else self.back_button[0]
        self.screen.blit(back_img, self.back_rect)

    def toggle_music(self):
        self.music_on = not self.music_on
        settings.settings["music_on"] = self.music_on
        settings.save_settings()
        self.music_channel.set_volume(self.volume / 100.0 if self.music_on else 0.0)

    def change_volume(self, delta):
        self.volume = max(0, min(100, self.volume + delta))
        settings.settings["volume"] = self.volume
        settings.save_settings()
        if self.music_on:
            self.music_channel.set_volume(self.volume / 100.0)

    def perform_reset_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write("0")

    def change_color(self, mouse_pos):
        for color, img in self.snake_color_selectors.items():
            selector_pos = self.snake_color_selector_coords[color]
            selector_rect = img.get_rect(topleft=selector_pos)
            if selector_rect.collidepoint(mouse_pos):
                self.selected_snake_color = color
                settings.settings["snake_color"] = color
                settings.save_settings()
                break

    def update_cursor(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_button = None
        self.hovered_settings_button = None
        self.hovered_customize_button = None
        self.hovered_credits_button = None

        if not self.in_settings and not self.in_customize and not self.in_credits:
            for (name, button_img), rect in zip(self.buttons, self.button_rects):
                if self.is_click_on_image(button_img, rect, mouse_pos):
                    self.hovered_button = name
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return
            
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif self.in_settings:
            if self.is_click_on_image(self.volume_controls["toggle_on"], self.music_toggle_rect, mouse_pos) or \
            self.is_click_on_image(self.volume_controls["toggle_off"], self.music_toggle_rect, mouse_pos):
                self.hovered_settings_button = "music_toggle"
            elif self.volume_down_rect.collidepoint(mouse_pos):
                self.hovered_settings_button = "volume_down"
            elif self.volume_up_rect.collidepoint(mouse_pos):
                self.hovered_settings_button = "volume_up"
            elif self.reset_rect.collidepoint(mouse_pos):
                self.hovered_settings_button = "reset"
            elif self.back_rect.collidepoint(mouse_pos):
                self.hovered_settings_button = "back"
            else:
                speed_rect = self.game_speeds[self.speed_states[self.current_speed_index]][0].get_rect(topleft=(443, 376))
                if speed_rect.collidepoint(mouse_pos):
                    self.hovered_settings_button = "speed"

            if self.hovered_settings_button:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        elif self.in_customize:
            hovered_on_selector = False
            for color, img in self.snake_color_selectors.items():
                selector_pos = self.snake_color_selector_coords[color]
                selector_rect = img.get_rect(topleft=selector_pos)
                if selector_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    hovered_on_selector = True
                    break

            if not hovered_on_selector:
                if self.back_rect.collidepoint(mouse_pos):
                    self.hovered_customize_button = "back"
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    self.hovered_customize_button = None
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        elif self.in_credits:
            if self.back_rect.collidepoint(mouse_pos):
                    self.hovered_credits_button = "back"
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                self.hovered_credits_button = None
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def is_click_on_image(self, button_img, button_rect, mouse_pos):
        if button_rect.collidepoint(mouse_pos):
            rel_x = mouse_pos[0] - button_rect.left
            rel_y = mouse_pos[1] - button_rect.top

            pixel_alpha = button_img.get_at((rel_x, rel_y)).a
            if pixel_alpha > 0: 
                return True
        return False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Main Menu Events
                if not self.in_settings and not self.in_customize and not self.in_credits:
                    if self.is_click_on_image(self.buttons[0][1], self.button_rects[0], event.pos):  # Play
                        return 'play'
                    elif self.is_click_on_image(self.buttons[1][1], self.button_rects[1], event.pos):  # Settings
                        self.in_settings = True
                        self.settings_open_time = time.time()
                    elif self.is_click_on_image(self.buttons[2][1], self.button_rects[2], event.pos):  # Customize
                        self.in_customize = True
                    elif self.is_click_on_image(self.buttons[3][1], self.button_rects[3], event.pos):  # Credits
                        self.in_credits = True
                        self.credits_open_time = time.time()
                    elif self.is_click_on_image(self.buttons[-1][1], self.button_rects[-1], event.pos):  # Exit
                        pygame.quit()
                        sys.exit()
                # Settings UI Events
                if self.in_settings:
                    if time.time() - self.settings_open_time < self.settings_click_lockout_duration:
                        continue
                    if self.speed_rect.collidepoint(event.pos):
                        self.current_speed_index = (self.current_speed_index + 1) % len(self.speed_states)
                        settings.settings["game_speed"] = self.speed_states[self.current_speed_index]
                        settings.save_settings()
                    if self.music_toggle_rect.collidepoint(event.pos):
                        self.toggle_music()
                    if self.volume_down_rect.collidepoint(event.pos):
                        self.change_volume(-10)
                    if self.volume_up_rect.collidepoint(event.pos):
                        self.change_volume(+10)
                    if self.reset_rect.collidepoint(event.pos):
                        self.perform_reset_high_score()
                    if self.back_rect.collidepoint(event.pos):
                        settings.save_settings()
                        self.in_settings = False
                # Customize UI Events
                if self.in_customize:
                    self.change_color(event.pos)
                    if self.back_rect.collidepoint(event.pos):
                        self.in_customize = False
                # Credits UI Events
                if self.in_credits:
                    if time.time() - self.credits_open_time < self.credits_click_lockout_duration:
                        continue
                    if self.back_rect.collidepoint(event.pos):
                        self.in_credits = False
            # Exiting UI's
            elif event.type == pygame.KEYDOWN:
                if self.in_settings and event.key == pygame.K_ESCAPE:
                    settings.save_settings()
                    self.in_settings = False
                if self.in_customize and event.key == pygame.K_ESCAPE:
                    settings.save_settings()
                    self.in_customize = False
                if self.in_credits and event.key == pygame.K_ESCAPE:
                    self.in_credits = False

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

    def fade_in(self, duration_ms=1000):
        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))

        steps = 50
        delay = duration_ms / steps / 1000
        target_volume = settings.settings["volume"] / 100.0

        for i in range(steps + 1):
            alpha = 255 - int(i / steps * 255)
            fade_surface.set_alpha(alpha)
            
            if settings.settings["music_on"]:
                volume = i / steps * target_volume
                self.music_channel.set_volume(volume)

            self.update_background()
            self.draw_menu()
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)
            time.sleep(delay)

    def fade_out_music(self, duration_ms=1000):
        self.music_channel.fadeout(duration_ms)

    def run(self):
        # Reset music properly before fade-in
        self.music_channel.stop()
        self.music_channel.set_volume(0.0)
        self.music_channel.play(self.menu_music, loops=-1)
        
        self.fade_in(duration_ms=1000)

        while self.running:
            action = self.handle_events()

            # Clicking "Play"
            if action == 'play':
                settings.load_settings()
                self.fade_out_music(1000)
                self.fade_out()
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.hovered_button = None
                return

            self.update_cursor()
            self.update_background()

            # Displaying UI's
            if self.in_settings:
                self.draw_settings()
            elif self.in_customize:
                self.draw_customize()
            elif self.in_credits:
                self.draw_credits()
            else:
                self.draw_menu()

            pygame.display.flip()
            self.clock.tick(60)