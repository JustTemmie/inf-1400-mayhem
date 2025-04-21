from pyglet.math import Vec2, Vec3
from pyglet.window import key
from collections import namedtuple

import logging
import os

"""
    Client settings, these may be different from user to user
"""
mouse_movement: bool = True
mouse_virtual_joystick_deadzone: float = 0.075 # percentage from 0 to 1

key_binds = namedtuple("keybinds", ["vertical", "horizontal", "thrust", "shoot"])

KEY_BINDS = key_binds(
            [key.UP, key.DOWN], # vertical
            [key.LEFT, key.RIGHT], # horizontal
            key.LSHIFT, # thrust
            key.SPACE)  # shoot

target_refresh_rate: int = 60
display_resolution = Vec2(1920, 1080)
FOV: float = 80
VSYNC: bool = False

LOG_LEVEL = logging.INFO

"""
    Server settings, these should be the same for all players
"""
SERVER_ADDRESS: str = "example.com"
SERVER_TEST_ADDRESS: str = "127.0.0.1"
SERVER_PORT: int = 27827

target_physics_rate: int = 60

air_friction = 0.95 # float from 0 to 1, where 1 is 100%, really shouldn't ever be set above 10%
gravity = Vec3(0, 0, 0) # earth's gravity would be Vec3(0, 0, -9.8), but since we're in space, that makes no sense

rear_thrust_force: float = 500
rotation_thrust_force: float = 150_000

SHOOTING_INTERVAL = 0.2
BULLET_SPEED = 30
