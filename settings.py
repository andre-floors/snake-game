# Settings is done through a JSON file in order for the game to save the settings even after restarting.

import json
import os

# Default settings
default_settings = {
    "music_on": True,
    "volume": 50,
    "game_speed": "normal"
}

SETTINGS_FILE = "settings.json"

# Load settings from file
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return default_settings.copy()
    return default_settings.copy()

# Save current settings to file
def save_settings():
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

# Game speed timing values
SPEED_VALUES = {
    "slow": 0.20,
    "normal": 0.15,
    "fast": 0.10
}

# Load current settings at module import
settings = load_settings()

# Easy access shortcuts
music_on = settings["music_on"]
volume = settings["volume"]
game_speed = settings["game_speed"]