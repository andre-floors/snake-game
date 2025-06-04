# This file houses the code for the food spawning algorithm

import pygame
import random
import math

class Food:
    def __init__(self, grid_width, grid_height, snake_positions):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.image_normal = pygame.image.load("assets/images/game/food.png").convert_alpha()
        self.image_normal.set_colorkey((255, 255, 255))
        self.image_normal = pygame.transform.scale(self.image_normal, (25, 25))

        self.image_bonus = pygame.image.load("assets/images/game/bonus_food.png").convert_alpha()
        self.image_bonus.set_colorkey((255, 255, 255))
        self.image_bonus = pygame.transform.scale(self.image_bonus, (25, 25))

        self.is_bonus = False
        self.image = self.image_normal
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        while True:
            col = random.randint(1, self.grid_width)
            row = random.randint(1, self.grid_height)
            if (col, row) not in snake_positions:
                return (col, row)

    def respawn(self, snake_positions):
        self.position = self.random_position(snake_positions)
        self.is_bonus = random.random() < 0.2
        self.image = self.image_bonus if self.is_bonus else self.image_normal

    def get_animated_image(self):
        # Bounce animation using sine wave
        t = pygame.time.get_ticks() / 300.0
        scale = 1.0 + 0.1 * math.sin(t)  # 0.9 to 1.1 scale range
        size = int(25 * scale)
        # Animate currently active food image (normal or bonus)
        scaled_img = pygame.transform.smoothscale(self.image, (size, size))
        return scaled_img, size