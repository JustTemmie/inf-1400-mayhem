"""
Contains the Obstacle class
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Entity3D import Entity3D
from mayhem.entities.Bullet import Bullet

class Obstacle(Entity3D):
    """
    Generic obstacle class for interactions with the player
    """
    def engine_process(self, delta):
        self.check_for_collision(delta)
    
    def handle_collision(self, entity: Entity3D, delta):
        """
        By default, all obstacles should collide with bullets.

        Player collision is done within the player itself.
        """
        if isinstance(entity, Bullet):
            entity.free()