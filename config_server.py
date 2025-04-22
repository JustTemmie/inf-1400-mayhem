"""
    Server settings, these are intended to be the same for all players
"""

from pyglet.math import Vec2, Vec3
from pyglet.window import key
from collections import namedtuple

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

FUEL_RATE = 1  # Fuel per second
