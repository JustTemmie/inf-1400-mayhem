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

SHOOTING_INTERVAL = 0.25
BULLET_SPEED = 50

FUEL_RATE = 1  # Fuel per seconod
STARTING_FUEL = 80
MAX_FUEL = 100
BATTERY_RECHARGING_AMOUNT = 60
BATTERY_SPAWN_COOLDOWN = 15
MAX_BATTERY_COUNT = 5

GRAVITATIONAL_CONSTANT = 6.67*10**-11
