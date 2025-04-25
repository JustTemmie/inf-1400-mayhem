"""
Contains the MovementArrow class.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Window import Window
from engine.core.Entity2D import Entity2D
from engine.core.Input import Input
from engine.core_ext.Colour import Colour
from mayhem.entities2D.HUD.MovementReticle import MovementReticle

import pyglet
import math

class MovementArrow(Entity2D):
    """
    Simple entity that draws an arrow from the centre of the screen to the mouse, with size depending on distance.
    """
    def user_instantiate(self):
        
        middle = Window.size / 2
        
        self.arrow = pyglet.shapes.Line(middle.x, middle.y, 0, 0, 5, color=Colour.RED, batch=Entity2D.game_object.UI_batch)
        self.arrow_head = pyglet.shapes.Triangle(10, 10, 190, 10, 100, 150, color=Colour.RED, batch=Entity2D.game_object.UI_batch)

    def on_resize(self):
        middle = Window.size / 2
        
        self.arrow.x = middle.x
        self.arrow.y = middle.y
    
    def prepare_draw(self, delta):
        if MovementReticle.is_mouse_inside():
            self.arrow.visible = False
            self.arrow_head.visible = False
            return

        self.arrow.visible = True
        self.arrow_head.visible = True
        
        middle = Window.size / 2
        angle = math.atan2(Input.mouse.y - middle.y, Input.mouse.x - middle.x)
        
        size_modifier = max(15, math.sqrt((Input.mouse - middle).length()))
        arrow_head_length = size_modifier / 1.5
        arrow_head_width = arrow_head_length * 2


        self.arrow.x2 = Input.mouse.x
        self.arrow.y2 = Input.mouse.y
        self.arrow.thickness = size_modifier / 3


        self.arrow_head.x = Input.mouse.x - arrow_head_width * math.cos(angle + math.pi / 6)
        self.arrow_head.y = Input.mouse.y - arrow_head_width * math.sin(angle + math.pi / 6)
        self.arrow_head.x2 = Input.mouse.x + arrow_head_length * math.cos(angle)
        self.arrow_head.y2 = Input.mouse.y + arrow_head_length * math.sin(angle)
        self.arrow_head.x3 = Input.mouse.x - arrow_head_width * math.cos(angle - math.pi / 6)
        self.arrow_head.y3 = Input.mouse.y - arrow_head_width * math.sin(angle - math.pi / 6)
