from pyglet.math import Vec2, Vec3
from pyglet.window import key
from collections import namedtuple

import logging
import os

SERVER_ADDRESS: str = "example.com"
SERVER_TEST_ADDRESS: str = "127.0.0.1"
SERVER_PORT: int = 27827

air_friction = 0.035 # float from 0 to 1, where 1 is 100%, really shouldn't ever be set above 10%
gravity = Vec3(0, 0, 0) # earth's gravity would be Vec3(0, -9.8, 0)

rear_thrust_force: float = 3000
side_thrust_force: float = 800
roll_thrust_force: float = 30

SHOOTING_INTERVAL = 0.2

LOG_LEVEL = logging.WARN

BULLET_SPEED = 30

# display resolution has 0 effect on the simulation or rendering, and is just used to set the window size
# canvas resolution is used by the camera for rendering, but will change the simulation if AUTO_GENERATE_BOUNDRY_CORNERS is set to true
# display_resolution = Vector2(1920, 1080)
display_resolution = Vec2(1920, 1080)
# canvas_resolution = Vector2(1920, 1080) maybe we won't have to use this for opengl shenanigans

target_refresh_rate: int = 60
target_physics_rate: int = 60
FOV: float = 80
VSYNC: bool = False

mouse_movement: bool = False # WIP
virtual_joystick_deadzone: float = 0.1 # percentage from 0 to 1


key_binds = namedtuple("keybinds", ["vertical", "horizontal", "pitch", "yaw", "roll", "thrust", "shoot"])

if os.getenv("LAYOUT") == "us(colemak)":
    KEY_BINDS = key_binds(
        [key.W, key.R], # vertical
        [key.A, key.S], # horizontal
        [key.LEFT, key.RIGHT], # pitch
        [key.UP, key.DOWN], # yaw
        [key.Q, key.F], # roll
        key.LSHIFT, # thrust
        key.SPACE)  # shoot
else: # assume qwerty
    KEY_BINDS = key_binds(
    [key.W, key.S], # vertical
    [key.A, key.D], # horizontal
    [key.LEFT, key.RIGHT], # pitch
    [key.UP, key.DOWN], # yaw
    [key.Q, key.E], # roll
    key.LSHIFT, # thrust
    key.SPACE)  # shoot
