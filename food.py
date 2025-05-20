import pygame
import random

class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.image = pygame.image.load("assets/food.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.position = self.random_position()

    def random_position(self):
        col = random.randint(0, self.grid_width - 1)
        row = random.randint(0, self.grid_height - 1)
        return (col, row)