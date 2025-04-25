"""
Contains the battery class
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D
from engine.extras.Utils import Utils
from mayhem.entities.pickups.Pickup import Pickup
from mayhem.entities.players.LocalPlayer import LocalPlayer

import config

from pyglet.math import Vec3

import pyglet
import math
import logging

class Battery(Pickup):
    """
    3D pickup entity to allow the player to recharge.
    """
    
    # list of all existing batteries
    batteries = []
    
    def user_init(self):
        self.mass = 5  # kg
        self.area = 1  # m^2, affects the objects interaction with air
        self.ignore_friction: bool = True
        self.rotation_velocity = Vec3(0, 2, 0)
        self.rotation = Vec3(math.pi / 2, 0, 0)

        Battery.current_battery = self
    
    def user_instantiate(self):
        self.hitboxes.append(Hitsphere3D(self.pos, Vec3(0, 0, 0), 3))
        
        model_scene = pyglet.resource.scene(Utils.get_model_path("battery"))

        self.model = model_scene.create_models(batch=Pickup.game_object.main_batch)[0]

    def picked_up(self, player: LocalPlayer):
        player.fuel += config.BATTERY_RECHARGING_AMOUNT
        player.fuel = min(player.fuel, config.MAX_FUEL)

        if self in Battery.batteries:
            Battery.batteries.remove(self)
        
        self.free()

        #TODO
        # play sound

    def spawn(self, radius: float):
        if len(Battery.batteries) >= config.MAX_BATTERY_COUNT:
            self.call_deferred(lambda: self.free())
            return
        
        self.pos = Utils.get_random_normalized_3D_vector() * radius
        Battery.batteries.append(self)