"""
Generic pickup class for interactions with the player
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Entity3D import Entity3D

import abc

class Pickup(Entity3D):
    @abc.abstractmethod
    def picked_up(self, player):
        """
        Called whenever the player picks up the object, remember to free it yourself.
        """
        pass