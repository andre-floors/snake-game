# Settings is done through a JSON file in order for the game to save the settings even after restarting.

import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "music_on": True,
    "volume": 50,
    "game_speed": "normal"
}

SPEED_VALUES = {
    "slow": 0.20,
    "normal": 0.15,
    "fast": 0.07
}

# Holds the in-memory settings
settings = DEFAULT_SETTINGS.copy()

def load_settings():
    global settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    else:
        save_settings()

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

load_settings()