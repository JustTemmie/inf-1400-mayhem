"""
    Server settings, these are intended to be the same for all players
"""

SERVER_ADDRESS: str = "hetzner.beaver.mom"
SERVER_PORT: int = 27827

SERVER_TIMEOUT = 10

target_physics_rate: int = 60

air_friction = 0.95 # float from 0 to 1, where 1 is 100%, really shouldn't ever be set above 10%

rear_thrust_force: float = 500
rotation_thrust_force: float = 150_000

SHOOTING_INTERVAL = 0.2
BULLET_SPEED = 30

FUEL_RATE = 1  # Fuel per seconod

GRAVITATIONAL_CONSTANT = 6.67*10**-5
