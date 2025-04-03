from pyglet.math import Vec2, Vec3
from pyglet.window import key

import logging
from collections import namedtuple

SERVER_ADDRESS: str = "example.com"
SERVER_TEST_ADDRESS: str = "127.0.0.1"
SERVER_PORT: int = 27827

air_friction = 0.1 # float from 0 to 1, where 1 is 100%, really shouldn't ever be set above 10%
gravity = Vec3(0, 0, 0) # earth's gravity would be Vec3(0, -9.8, 0)
thrust_force: float = 1000

LOG_LEVEL = logging.WARN

# display resolution has 0 effect on the simulation or rendering, and is just used to set the window size
# canvas resolution is used by the camera for rendering, but will change the simulation if AUTO_GENERATE_BOUNDRY_CORNERS is set to true
# display_resolution = Vector2(1920, 1080)
display_resolution = Vec2(1920, 1080)
# canvas_resolution = Vector2(1920, 1080) maybe we won't have to use this for opengl shenanigans

target_refresh_rate = 60
target_physics_rate = 60
FOV = 80
VSYNC = False


key_binds = namedtuple("keybinds", ["vertical", "horizontal", "roll", "thrust", "shoot"])
KEY_BINDS = key_binds(
    [key.W, key.R], # vertical
    [key.A, key.S], # horizontal
    [key.Q, key.F], # roll
    key.LSHIFT, # thrust
    key.SPACE)  # shoot
