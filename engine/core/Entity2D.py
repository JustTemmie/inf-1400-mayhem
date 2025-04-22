"""
2d entities ( write more later )
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Entity import Entity

from pyglet.math import Vec2

class Entity2D(Entity):
    all_2D_entities: list["Entity2D"] = []

    def __init__(self):
        super().__init__()
        self.pos: Vec2 = Vec2(0, 0)  # x, y
        self.velocity: Vec2 = Vec2(0, 0)  # x, y
        self.acceleration: Vec2 = Vec2(0, 0)  # x, y

        # euler angles
        self.rotation: Vec2 = Vec2(0, 0)  # x, y
        self.rotation_velocity: Vec2 = Vec2(0, 0)  # x, y
        self.rotation_acceleration: Vec2 = Vec2(0, 0)  # x, y

        self.render_batch = None
        self.size: Vec2 = Vec2(0, 0) # not required to be used by an entity

        self.user_init()

    def instantiate(self):
        self.render_batch = Entity.game_object.UI_batch
        Entity2D.all_2D_entities.append(self)
        super().instantiate()
    
    def prepare_draw(self, delta):
        pass

    def handle_physics(self, delta: float, air_friction: float, gravity: Vec2):
        """
        Handles physics, called within the engine, not meant to be interacted with by the user
        """
        self.acceleration += gravity
        self.velocity += self.acceleration * delta
        self.velocity *= 1 - air_friction
        self.pos += self.velocity * delta

        self.rotation_velocity += self.rotation_acceleration * delta
        self.rotation_velocity *= 1 - air_friction
        self.rotation += self.rotation_velocity * delta

        # we don't actually want to keep acceleration
        self.acceleration = Vec2(0, 0)
        self.rotation_acceleration = Vec2(0, 0)

    def free(self):
        Entity2D.all_2D_entities.remove(self)
        return super().free()