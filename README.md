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
   ```
2. Install pygame (if not installed) by entering the command into cmd (Command Prompt):
   ```
   pip install pygame

3. Run the game
   ```
   python main.py

---

## How To Play

1. Use **W** (Up), **A** (Left), **S** (Down), and **D** (Right) keys to control the snake.
2. Eat the food to grow longer.
3. Avoid running into walls or the snake’s own body.
4. The game ends if a collision occurs.

---

## Project Structure
  ```
  snake-game/
  │
  ├── assets/                  # Image assets for snake and food
  │   ├── snake_head1.png
  │   ├── snake_body1.png
  │   ├── snake_tail1.png
  │   └── food.png
  │
  ├── main.py                  # Main game loop and initialization
  ├── snake.py                 # Snake class with movement, collision, and rendering logic
  ├── food.py                  # Food class handling random spawning
  └── README.md                # Project documentation (this file)
  ```

---

## Future Improvements

- Add sound effects and background music.
- Improve UI and add start/game over screens.
- Add difficulty levels and speed increase mechanics.

---

## License

This project is open-source and free to use for educational purposes.

---

**Developed by Andre Ryan F. Flores**<br />
for Data Structures & Algorithms – BSIT 2-2<br />
Cavite State University - Bacoor City Campus
