from collections import namedtuple

import pyglet

mousePosTuple = namedtuple("mouse", ["x", "y"])

class Input():
    keyboard_keys = pyglet.window.key.KeyStateHandler()
    mouse: mousePosTuple = mousePosTuple(0, 0)
    
    def on_mouse_motion(x, y, dx, dy):
        mouse = mousePosTuple(x, y)