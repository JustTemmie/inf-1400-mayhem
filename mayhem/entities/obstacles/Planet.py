"""
Contains the planet class.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.extras.Utils import Utils
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D
from mayhem.entities.obstacles.Obstacle import Obstacle

from pyglet.math import Vec3

import pyglet


class Planet(Obstacle):
    """
    Class for the massive planet you see in the game world.
    """
    
    def user_init(self):
        self.mass = 6*10**14  # kg
        self.area = 1  # m^2, affects the objects interaction with air
        self.ignore_friction: bool = True
        self.rotation_velocity = Vec3(0.02, 0, 0)
        self.rotation = Vec3(0, 0.28, 0.74)
    
    def user_instantiate(self):
        self.hitboxes.append(Hitsphere3D(self.pos, Vec3(0, 0, 0), 200))
        
        model_scene = pyglet.resource.scene(Utils.get_model_path("planet"))

        self.model = model_scene.create_models(batch=Obstacle.game_object.main_batch)[0]

