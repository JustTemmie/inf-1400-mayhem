"""
The minimum required to create a 3D object.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Utils import Utils
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D
from mayhem.entities.pickups.Pickup import Pickup
from mayhem.entities.players.LocalPlayer import LocalPlayer

from pyglet.math import Vec3

import pyglet
import math

class Battery(Pickup):
    current_battery = None
    
    def user_init(self):
        self.mass = 5  # kg
        self.area = 1  # m^2, affects the objects interaction with air
        self.ignore_friction: bool = True
        self.rotation_velocity = Vec3(0, 2, 0)
        self.rotation = Vec3(math.pi / 2, 0, 0)

        Battery.current_battery = self
    
    def user_instantiate(self):
        self.hitboxes.append(Hitsphere3D(self.pos, Vec3(0, 0, 0), .5))
        
        model_scene = pyglet.resource.scene(Utils.get_model_path("battery"))

        self.model = model_scene.create_models(batch=Pickup.game_object.main_batch)[0]

    def picked_up(self, player: LocalPlayer):
        player.fuel = 100
        Battery.current_battery = None
        self.free()
        #TODO
        # play sound
