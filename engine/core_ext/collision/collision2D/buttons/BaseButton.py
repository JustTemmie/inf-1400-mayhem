"""
File containing the BaseButton class and the DrawMode enum
Authors: JustTemmie (i'll replace names at handin)
"""


# THIS WILL NOT WORK UNTIL THE colliding_with() FUNCTION IS FINISHED

from engine.core.Entity2D import Entity2D
from engine.core.Input import Input
from engine.core_ext.collision.collision2D.Hitarea2D import Hitarea2D

from enum import Enum
from pyglet.math import Vec2
import pyglet.window.mouse as pyglet_mouse

import logging

class DrawMode(Enum):
    normal = 0
    pressed = 1
    hover = 2
    hover_and_pressed = 3
    disabled = 4

class BaseButton(Entity2D):
    """
    An abstract base class for other buttons, not intended for use by the end user
    """

    def __init__(self, hit_area_type: Hitarea2D):
        super().__init__()
        
        self.hit_area_type = hit_area_type
        self.hit_area: Hitarea2D 
        
        self.draw_mode: int = DrawMode.normal
        self.pressed: bool = False
        self.disabled: bool = False
        self.toggled: bool = False
        self.toggle_mode: bool = False
    
    def user_instantiate(self):
        if Vec2(0, 0) in [self.pos, self.size]:
            logging.warning(f"{self.__class__.__name__} button does not have pos or size {self.pos}, {self.size}, here be dragons")

        # create hit_area instance here
    
    def on_button_down(self):
        """
        Called when the button is initially pressed down
        """
        pass
    
    def on_pressed(self):
        """
        Called when the button is released, and the mouse is still ontop of the button
        """
        pass
    
    def on_released(self):
        """
        Called when the button is released
        """
        pass
    
    def on_toggled(self, value: bool):
        """
        Replaces on_pressed if the button is set to toggle_mode
        """
        pass
    
    def disable(self, value: bool):
        """
        Call if you want to update the disabled property on the button
        """
        self.disabled = value
        if self.disable:
            self.draw_mode = DrawMode.disabled
        else:
            self.draw_mode = DrawMode.normal
        
    def process(self, delta):
        if self.disabled:
            return

        self.draw_mode = DrawMode.normal
        self.hit_area.update_object(self.pos, self.rotation)
        
        # if mouse is within button
        if self.hit_area.colliding_with(Input.mouse_hit_area):
            self.draw_mode = DrawMode.hover
            
            if pyglet_mouse.LEFT in Input.active_mouse_buttons:
                if not self.pressed:
                    self.on_button_down()
                self.pressed = True

        # if not holding left
        if pyglet_mouse.LEFT not in Input.active_mouse_buttons:
            if self.hit_area.colliding_with(Input.mouse_hit_area):
                if self.toggle_mode:
                    self.toggle_mode = not self.toggle_mode
                    self.on_toggled(self.toggle_mode)
                else:
                    self.on_pressed()
            
            if self.pressed:
                self.on_released()
            self.pressed = False
        
        if self.pressed:
            self.draw_mode += 1 # turns 0 to 1, and 2 to 3