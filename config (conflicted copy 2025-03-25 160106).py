from pyglet.math import Vec2

SERVER_ADDRESS: str = "example.com"
SERVER_PORT: int = 27827

LOG_DEBUG_EVENTS = False

# display resolution has 0 effect on the simulation or rendering, and is just used to set the window size
# canvas resolution is used by the camera for rendering, but will change the simulation if AUTO_GENERATE_BOUNDRY_CORNERS is set to true
# display_resolution = Vector2(1920, 1080)
display_resolution = Vec2(1920, 1080)
# canvas_resolution = Vector2(1920, 1080) maybe we won't have to use this for opengl shenanigans

target_refresh_rate = 120
target_physics_rate = 30
VSYNC = False