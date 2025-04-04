from collections import namedtuple
from pyglet.math import Vec2

import pyglet

mousePosTuple = namedtuple("mouse", ["x", "y"])

class Input():
    keyboard_keys = pyglet.window.key.KeyStateHandler()
    mouse: Vec2 = Vec2(0, 0)
    
    def on_mouse_motion(x, y, dx, dy):
        Input.mouse = Vec2(x, y)