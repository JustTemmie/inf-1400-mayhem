from pyglet.math import Vec2
from pyglet.window import key

SERVER_ADDRESS: str = "example.com"
SERVER_TEST_ADDRESS: str = "127.0.0.1"
SERVER_PORT: int = 27827

LOG_DEBUG_EVENTS = False

# display resolution has 0 effect on the simulation or rendering, and is just used to set the window size
# canvas resolution is used by the camera for rendering, but will change the simulation if AUTO_GENERATE_BOUNDRY_CORNERS is set to true
# display_resolution = Vector2(1920, 1080)
display_resolution = Vec2(1920, 1080)
# canvas_resolution = Vector2(1920, 1080) maybe we won't have to use this for opengl shenanigans

target_refresh_rate = 360
target_physics_rate = 30
VSYNC = False


KEY_BINDS = {"pitch": [key.S, key.W],
             "yaw": [key.E, key.Q],
             "roll": [key.A, key.D],
             "thrust": key.LSHIFT,
             "shoot": key.SPACE}
