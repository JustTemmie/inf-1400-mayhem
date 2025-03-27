from engine.core_ext.Entity import Entity

from pyglet.gl import glEnable, GL_DEPTH_TEST, GL_CULL_FACE
from pyglet.math import Mat4, Vec3

import pyglet
import typing
import logging

if typing.TYPE_CHECKING:
    from engine.core.Game import Game

class Entity3D(Entity):
    all_3D_entities: list["Entity3D"] = []

    def __init__(self):
        super().__init__()
        self.pos: Vec3 = Vec3(0, 0, 0) # x, y, z
        self.velocity: Vec3 = Vec3(0, 0, 0) # x, y, z
        self.acceleration: Vec3 = Vec3(0, 0, 0) # x, y, z
        
        self.rotation: Vec3 = Vec3(0, 0, 0) # x, y, z
        self.rotation_velocity: Vec3 = Vec3(0, 0, 0) # x, y, z
        self.rotation_acceleration: Vec3 = Vec3(0, 0, 0) # x, y, z
        
        self.model: pyglet.model.Scene
        
        self.user_init()

    def instantiate(self, game):
        super().instantiate(game)
        self.all_3D_entities.append(self)
    
    # https://github.com/pyglet/pyglet/blob/fb1b992e31d712da43409e2910d2f07ea7e1177f/examples/model/model.py
    def draw(self):
        if not self.model:
            logging.warning(f"{self} does not have a set model, ignoring")
            return
        
        # note that Y is up
        rot_x = Mat4.from_rotation(self.rotation.x, Vec3(1, 0, 0))
        rot_y = Mat4.from_rotation(self.rotation.y, Vec3(0, 1, 0))
        rot_z = Mat4.from_rotation(self.rotation.z, Vec3(0, 0, 1))

        trans = Mat4.from_translation(self.pos)
        
        self.model.matrix = trans @ rot_z @ rot_x @ rot_y
    
    def handle_physics(self, delta: float, air_friction: float = 0, gravity: Vec3 = Vec3(0, 0, 0)):
        """
            Handles physics, call it once per tick on your entity3D.
        """
        self.acceleration *= (1 - air_friction)
        self.velocity += (self.acceleration + gravity) * delta
        self.pos += self.velocity * delta
        
        self.rotation_velocity *= (1 - air_friction)
        self.rotation += self.rotation_velocity * delta
    
    def look_at(self, pos: Vec3):
        """
            Make the entity turn to look at the given position.
        """
        look_towards: Vec3 = self.pos - pos
        # uhh, math here i guess

    
    @classmethod
    def get_all_3D_entities(self):
        return self.all_3D_entities
