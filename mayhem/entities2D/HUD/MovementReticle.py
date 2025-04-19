"""
Very simple entity that just draws the "deadzone" for the digital analogue stick.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Window import Window
from engine.core.Input import Input
from engine.core.Entity2D import Entity2D

import config

from pyglet.math import Vec2

import pyglet


class MovementReticle(Entity2D):
    def user_instantiate(self):
        if config.mouse_movement:
            ellipse_size = self.get_ellipse_dimensions()

            self.middle_ellipse = pyglet.shapes.Ellipse(
                x=Window.size.x / 2,
                y=Window.size.y / 2,
                a=ellipse_size.x,
                b=ellipse_size.y,
                color=(255, 80, 80, 55),
                batch=self.render_batch,
            )
    
    def get_ellipse_dimensions(self):
        radius_x = Window.size.x * config.mouse_virtual_joystick_deadzone / 2
        radius_y = Window.size.y * config.mouse_virtual_joystick_deadzone / 2
        
        return Vec2(radius_x, radius_y)
    
    def prepare_draw(self, delta):
        if config.mouse_movement:
            self.middle_ellipse.position = Vec2(
                x=Window.size.x / 2,
                y=Window.size.y / 2
            )
            
            ellipse_size = self.get_ellipse_dimensions()
            
            self.middle_ellipse.a = ellipse_size.x
            self.middle_ellipse.b = ellipse_size.y
    
    def is_mouse_inside() -> bool:
        if not config.mouse_movement:
            return False
        
        # generates a value between -1 and 1 for both axes
        standardized_mouse_position: Vec2 = (Input.mouse - Window.size / 2) / (Window.size / 2)
        
        # caps the length to one
        magnitude = max(1, standardized_mouse_position.length()) # don't divide by values under 1
        normalized_mouse_position = standardized_mouse_position / magnitude
        
        return normalized_mouse_position.length() < config.mouse_virtual_joystick_deadzone