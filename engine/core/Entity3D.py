from engine.core.Entity import Entity

from pyglet.gl import glEnable, GL_DEPTH_TEST, GL_CULL_FACE
from pyglet.math import Mat4, Vec3, Quaternion

import pyglet
import typing
import math
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
        
        # euler angles
        self.rotation: Vec3 = Vec3(0, 0, 0) # x, y, z
        self.rotation_velocity: Vec3 = Vec3(0, 0, 0) # x, y, z
        self.rotation_acceleration: Vec3 = Vec3(0, 0, 0) # x, y, z
        
        self.model: pyglet.model.Scene
        
        self.user_init()

    def instantiate(self, game):
        super().instantiate(game)
        Entity3D.all_3D_entities.append(self)
    
    # https://github.com/pyglet/pyglet/blob/fb1b992e31d712da43409e2910d2f07ea7e1177f/examples/model/model.py
    def draw(self):
        if not self.model:
            logging.warning(f"{self} does not have a set model, ignoring")
            return
        
        # note that Z is up
        rot_x = Mat4.from_rotation(self.rotation.x, Vec3(1, 0, 0))
        rot_y = Mat4.from_rotation(self.rotation.y, Vec3(0, 0, 1))
        rot_z = Mat4.from_rotation(self.rotation.z, Vec3(0, 1, 0))

        trans = Mat4.from_translation(self.pos)

        self.model.matrix = trans @ rot_y @ rot_x @ rot_z
    
    def handle_physics(self, delta: float, air_friction: float, gravity: Vec3):
        """
            Handles physics, called within the engine, not meant to be interacted with by the user
        """        
        self.acceleration += gravity
        self.velocity += self.acceleration * delta
        self.velocity *= (1 - air_friction)
        self.pos += self.velocity * delta

        self.rotation_velocity += self.rotation_acceleration * delta
        self.rotation_velocity *= (1 - air_friction)
        self.rotation += self.rotation_velocity * delta

        # we don't actually want to keep acceleration
        self.acceleration = Vec3(0, 0, 0) 
        self.rotation_acceleration = Vec3(0, 0, 0) 

        # print(self.rotation)
        # self.rotation = (self.rotation + math.pi) % (math.pi * 2) - math.pi
    
    # i do NOT feel like doing math as i'm writing this
    # so the up and right vector functions are modified from output from chat.uit.no, see chatlogs/Compute Front Right Vecto.json
    def get_up_vector(self) -> Vec3:
        """
            Computes the up direction vector in world space, considering roll.
        """
        # Compute the up vector using pitch (rotation.x), yaw (rotation.y), and roll (rotation.z)
        up_x = -math.sin(self.rotation.z) * math.cos(self.rotation.y) - math.cos(self.rotation.z) * math.sin(self.rotation.x) * math.sin(self.rotation.y)
        up_y = -math.sin(self.rotation.z) * math.sin(self.rotation.y) + math.cos(self.rotation.z) * math.sin(self.rotation.x) * math.cos(self.rotation.y)
        up_z = math.cos(self.rotation.z) * math.cos(self.rotation.x)
        return Vec3(up_x, up_y, up_z).normalize()

    def get_right_vector(self) -> Vec3:
        """
            Computes the right direction vector in world space, considering roll.
        """
        right_x = math.cos(self.rotation.z) * math.cos(self.rotation.y) - math.sin(self.rotation.z) * math.sin(self.rotation.x) * math.sin(self.rotation.y)
        right_y = math.cos(self.rotation.z) * math.sin(self.rotation.y) + math.sin(self.rotation.z) * math.sin(self.rotation.x) * math.cos(self.rotation.y)
        right_z = -math.sin(self.rotation.z) * math.cos(self.rotation.x)

        return Vec3(right_x, right_y, right_z).normalize()

    def get_forward_vector(self) -> Vec3:
        """
            Computes the forward direction vector in world space.
        """
        forward_x = math.cos(self.rotation.x) * math.sin(self.rotation.y)
        forward_y = math.cos(self.rotation.x) * math.cos(self.rotation.y)
        forward_z = -math.sin(self.rotation.x)

        return Vec3(forward_x, forward_y, forward_z).normalize()
    
    def look_at(self, pos: Vec3):
        """
            Make the entity turn to look at the given position.
            Not implemented.
        """
        
        # i actually don't think we need this function, the camera already has this biult in
        
        look_towards: Vec3 = self.pos - pos
        # uhh, math here i guess

    
    @classmethod
    def get_all_3D_entities(self):
        return self.all_3D_entities
