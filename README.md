# Snake Game

A classic Snake game developed in Python using the [Pygame](https://www.pygame.org/) library.  
This project is created as a Data Structures & Algorithms activity in Cavite State University, created by Andre Ryan F. Flores.

---

## Table of Contents
- [About](#about)
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
  
---

## Installation

### Requirements:
- Python 3.x
- Pygame library

### Steps:

1. Download the latest release Snake_Game.exe from the Releases page on this repository.
2. Run the Snake_Game.exe file by double-clicking it.

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
  ├── assets/                  # Game assets
  │   ├── fonts/               # Fonts used in the game
  │   │   └── (font files here)
  │   ├── images/              # Images for snake, food, UI, etc.
  │   │   ├── snake_head_{color}.png
  │   │   ├── snake_body_{color}.png
  │   │   ├── snake_tail_{color}.png
  │   │   └── food.png
  │   └── sfx/                 # Sound effects and music
  │       └── (sound files here)
  │
  ├── main.py                  # Main game loop and initialization
  ├── snake.py                 # Snake class with movement, collision, and rendering logic
  ├── food.py                  # Food class handling random spawning
  ├── settings.py              # Settings management (load/save, configs)
  ├── settings.json            # JSON file storing persistent user settings
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
