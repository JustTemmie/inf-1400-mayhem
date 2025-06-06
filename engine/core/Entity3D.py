"""
Contains the 3D entity class.
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Entity import Entity

from pyglet.math import Mat4, Vec3

import pyglet
import math
import logging

class Entity3D(Entity):
    """
    3D entities are just entities, but specialized for a 3D environment 
    """

    all_3D_entities: list["Entity3D"] = []

    def __init__(self):
        super().__init__()
        self.pos: Vec3 = Vec3(0, 0, 0)  # x, y, z
        self.velocity: Vec3 = Vec3(0, 0, 0)  # x, y, z
        self.acceleration: Vec3 = Vec3(0, 0, 0)  # x, y, z

        # euler angles
        self.rotation: Vec3 = Vec3(0, 0, 0)  # x, y, z
        self.rotation_velocity: Vec3 = Vec3(0, 0, 0)  # x, y, z
        self.rotation_acceleration: Vec3 = Vec3(0, 0, 0)  # x, y, z

        self.collidable = True
        self.hitboxes = []

        self.model: pyglet.model.Scene

        self.user_init()

    def instantiate(self):
        Entity3D.all_3D_entities.append(self)
        super().instantiate()

    # https://github.com/pyglet/pyglet/blob/fb1b992e31d712da43409e2910d2f07ea7e1177f/examples/model/model.py
    def prepare_draw(self, delta):
        if not self.model:
            logging.warning(f"{self} does not have a set model, ignoring")
            return

        # note that Z is up, i'm pretty sure at least
        rot_x = Mat4.from_rotation(self.rotation.x, Vec3(1, 0, 0))
        rot_y = Mat4.from_rotation(self.rotation.y, Vec3(0, 0, 1))
        rot_z = Mat4.from_rotation(self.rotation.z, Vec3(0, 1, 0))

        trans = Mat4.from_translation(self.pos)

        self.model.matrix = trans @ (rot_z @ rot_y @ rot_x)

    def handle_physics(self, delta: float, air_friction: float):
        """
        Handles physics, called within the engine, not meant to be interacted with by the user.
        """
        drag = Vec3(0, 0, 0)
        if not self.ignore_friction:
            air_density = 1  # Since the game is in space, this is in fact zero, makeing the entire drag disapear
            drag_without_speed = (1 / 2) * self.drag_coeficient * air_density * self.area

            # Using abs to keep the the correct sign
            drag = Vec3(
                drag_without_speed * self.velocity.x * abs(self.velocity.x),
                drag_without_speed * self.velocity.y * abs(self.velocity.y),
                drag_without_speed * self.velocity.z * abs(self.velocity.z),
            )

        self.acceleration += self.get_gravity() / self.mass
        self.velocity += self.acceleration * delta - drag/self.mass  # Drag is allready multiplied with delta, because of the speed.
        self.pos += self.velocity * delta

        self.rotation_velocity += self.rotation_acceleration * delta
        if not self.ignore_friction:
            self.rotation_velocity *= 1 - air_friction
        self.rotation += self.rotation_velocity * delta

        # we don't actually want to keep acceleration
        self.acceleration = Vec3(0, 0, 0)
        self.rotation_acceleration = Vec3(0, 0, 0)

        # clamp all values between 0 and 2pi
        self.rotation = self.rotation % (math.pi * 2)

    def check_for_collision(self, delta: float):
        """
        Checks for collision, and calles "handle_collision" on every collision
        """
        for entity in Entity3D.all_3D_entities:
            if not entity.collidable or entity == self:
                continue

            for entity_hitbox in entity.hitboxes:
                for hitbox in self.hitboxes:
                    if entity_hitbox.colliding_with(hitbox):
                        self.handle_collision(entity, delta)

    def handle_collision(self, entity: "Entity3D", delta: float):
        """
        Handles a collision

        Parmetrs:
            entity: The entity that was collided with
            delta: Delta time
        """
        pass

    # i do NOT feel like doing math as i'm writing this
    # so the up and right vector functions are modified from output from chat.uit.no, see chatlogs/Compute Front Right Vecto.json
    def get_up_vector(self) -> Vec3:
        """
        Computes the upwards pointing vector from the entity.
        """
        up_x = math.sin(self.rotation.x) * math.sin(self.rotation.z) + math.cos(self.rotation.x) * math.cos(self.rotation.z) * math.sin(self.rotation.y)
        up_y = -math.cos(self.rotation.z) * math.sin(self.rotation.x) + math.sin(self.rotation.z) * math.sin(self.rotation.x) * math.cos(self.rotation.y)
        up_z = math.cos(self.rotation.x) * math.cos(self.rotation.y)

        return Vec3(up_x, up_y, up_z).normalize()

    def get_right_vector(self) -> Vec3:
        """
        Computes the right pointing vector from the entity.
        """
        right_x = math.cos(self.rotation.z) * math.cos(self.rotation.y) + math.sin(self.rotation.z) * math.sin(self.rotation.x) * math.sin(self.rotation.y)
        right_y = math.cos(self.rotation.z) * math.sin(self.rotation.y) - math.sin(self.rotation.z) * math.sin(self.rotation.x) * math.cos(self.rotation.y)
        right_z = -math.sin(self.rotation.z) * math.cos(self.rotation.x)

        return Vec3(right_x, right_y, right_z).normalize()

    def get_forward_vector(self) -> Vec3:
        """
        Computes the forward pointing vector from the entity.
        """
        forward_x = -math.cos(self.rotation.x) * math.sin(self.rotation.y) * math.cos(self.rotation.z) + math.sin(self.rotation.x) * math.sin(self.rotation.z)
        forward_y = math.cos(self.rotation.x) * math.cos(self.rotation.y) * math.cos(self.rotation.z) - math.sin(self.rotation.x) * math.sin(self.rotation.y) * math.sin(self.rotation.z)
        forward_z = -math.cos(self.rotation.x) * math.sin(self.rotation.z) + math.sin(self.rotation.x) * math.cos(self.rotation.z)

        return Vec3(forward_x, forward_y, forward_z)

    def is_rightside_up(self) -> bool:
        """
        Returns true if the object is rightside up, false if not
        """
        return (self.rotation.x < math.pi * 0.5 or self.rotation.x >= math.pi * 1.5)

    def free(self):
        if self.model:
            for vertex_list in self.model.vertex_lists:
                vertex_list.delete()
            del self.model
            self.model = None
        
        Entity3D.all_3D_entities.remove(self)
        return super().free()

    def get_gravity(self) -> Vec3:
        """
        Get the direction of gravity, usually a constant
        """
        return Vec3(0, 0, 0)