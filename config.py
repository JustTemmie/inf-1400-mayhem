from pyglet.math import Vec2, Vec3
from pyglet.window import key

import logging


SERVER_ADDRESS: str = "example.com"
SERVER_TEST_ADDRESS: str = "127.0.0.1"
SERVER_PORT: int = 27827

air_friction = 0 # float from 0 to 1, where 1 is 100%
gravity = Vec3(0, 0, 0) # earth's gravity would be Vec3(0, -9.8, 0)

LOG_LEVEL = logging.WARN

# display resolution has 0 effect on the simulation or rendering, and is just used to set the window size
# canvas resolution is used by the camera for rendering, but will change the simulation if AUTO_GENERATE_BOUNDRY_CORNERS is set to true
# display_resolution = Vector2(1920, 1080)
display_resolution = Vec2(1920, 1080)
# canvas_resolution = Vector2(1920, 1080) maybe we won't have to use this for opengl shenanigans

target_refresh_rate = 60
target_physics_rate = 30
FOV = 80
VSYNC = False


KEY_BINDS = {"pitch": [key.S, key.W],
            "yaw": [key.E, key.Q],
            "roll": [key.A, key.D],
            "thrust": key.LSHIFT,
            "shoot": key.SPACE}
