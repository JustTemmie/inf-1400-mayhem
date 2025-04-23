"""
    Client settings, these may be different from user to user
"""

from pyglet.math import Vec2, Vec3
from pyglet.window import key
from collections import namedtuple

import logging

mouse_movement: bool = True
mouse_virtual_joystick_deadzone: float = 0.075 # percentage from 0 to 1

target_refresh_rate: int = 60
display_resolution = Vec2(1920, 1080)
FOV: float = 80
VSYNC: bool = False

LOG_LEVEL = logging.INFO

MAX_UI_BAR_WIDTH = 0.2 # Compared to the screen width
UI_BAR_HEIGHT = 0.1 # Compared to the bar width

UI_BAR_MARGIN = 0.15 # Compared to the bar height

key_binds = namedtuple("keybinds", ["vertical", "horizontal", "thrust", "shoot"])
KEY_BINDS = key_binds(
            [key.UP, key.DOWN], # vertical
            [key.LEFT, key.RIGHT], # horizontal
            key.LSHIFT, # thrust
            key.SPACE)  # shoot


