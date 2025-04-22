"""
This module just assists in input handling
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core_ext.collision.collision2D.Hitbox2D import Hitbox2D

from collections import namedtuple
from pyglet.math import Vec2, Vec3

import pyglet

mousePosTuple = namedtuple("mouse", ["x", "y"])

class Input:
    keyboard_keys = pyglet.window.key.KeyStateHandler()
    mouse: Vec2 = Vec2(0, 0)
    active_mouse_buttons: list[bool] = []
    mouse_hit_area = Hitbox2D(Vec2(0, 0), 0, Vec2(0, 0), Vec2(1, 1))

    def on_mouse_motion(x, y, dx, dy):
        Input.mouse = Vec2(x, y)
        Input.mouse_hit_area.update(Input.mouse, 0)
    
    def on_mouse_press(x, y, button, modifiers):
        Input.active_mouse_buttons.append(button)
        
        Input.mouse = Vec2(x, y)
        Input.mouse_hit_area.update(Input.mouse, 0)

    def on_mouse_release(x, y, button, modifiers):
        if button in Input.active_mouse_buttons:
            Input.active_mouse_buttons.remove(button)
        
        Input.mouse = Vec2(x, y)
        Input.mouse_hit_area.update(Input.mouse, -1)
