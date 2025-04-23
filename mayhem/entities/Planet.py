"""
The minimum required to create a 3D object.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Utils import Utils
from engine.core.Entity3D import Entity3D
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D
from mayhem.entities.Bullet import Bullet

from pyglet.math import Vec3

import pyglet


class Planet(Entity3D):
    def user_init(self):
        self.mass = 80_000_000  # kg
        self.area = 1  # m^2, affects the objects interaction with air
        self.ignore_friction: bool = True
        self.rotation_velocity = Vec3(0.02, 0, 0)
        self.rotation = Vec3(0, 0.28, 0.74)
    
    def engine_process(self, delta):
        self.check_for_collision(delta)
    
    def handle_collision(self, entity: Entity3D, delta):
        if entity.__class__ == Bullet:
            entity.free()
    
    def user_instantiate(self):
        self.hitboxes.append(Hitsphere3D(self.pos, Vec3(0, 0, 0), 100))
        
        model_scene = pyglet.resource.scene(Utils.get_model_path("planet"))

        self.model = model_scene.create_models(batch=Entity3D.game_object.main_batch)[0]

