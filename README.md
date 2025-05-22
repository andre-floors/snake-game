# Snake Game

A classic Snake game developed in Python using the [Pygame](https://www.pygame.org/) library.  
This project is part of a Data Structures & Algorithms activity for BSIT 2-2, created by Andre Ryan F. Flores.

---

## Table of Contents
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## About

This Snake game implements a grid-based gameplay where the snake moves around collecting food to grow longer. The game includes:

- Directional movement controlled by **WASD** keys.
- Collision detection with the boundaries and the snake itself.
- Food spawning at random positions inside the grid.
- Snake growth mechanics upon eating food.
- Smooth rendering with custom snake assets for head, body, and tail.
  
---

## Features

- **Grid-based movement:** 30x26 grid cells, each 25x25 pixels.
- **Collision detection:** Walls and self-collision detection to end the game.
- **Food spawning:** Food randomly appears inside the play area.
- **Snake growth:** The snake length increases by 1 segment each time food is eaten.
- **Custom graphics:** Snake and food sprites with rotation for smooth animation.

---

## Installation

### Requirements:
- Python 3.x
- Pygame library

### Steps:

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/snake-game.git
   cd snake-game
2. Install pygame (if not installed) by entering the command into cmd (Command Prompt):
   ```
   pip install pygame

3. Run the game
   ```
   python main.py
