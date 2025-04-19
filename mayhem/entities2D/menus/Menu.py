"""
Very simple entity that just displays the player's score in the top left of the screen.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Window import Window
from engine.core.Entity2D import Entity2D
from mayhem.entities.players.LocalPlayer import LocalPlayer


class Menu:
    def __init__(self):
        self.entity_elements: list[Entity2D]
    
    def display(self):
        pass