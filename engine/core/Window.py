"""
Contains the Window class
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Camera import Camera
from engine.core.Entity import Entity

import config

from pyglet.gl import *
from pyglet.math import Mat4, Vec2

import pyglet

class Window(pyglet.window.Window):
    """
    Used heavily in rendering the game, do NOT extend this class.

    You can interact with an instanced version in your game's game.window variable.
    """
    size: Vec2 = config.display_resolution

    def __init__(self):
        gl_config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)

        super().__init__(
            Window.size.x, Window.size.y,
            resizable=True, visible=False,
            config=gl_config, vsync=config.VSYNC,
            caption="Mayhem (3D!!)",
        )

        # init the camera
        Camera(self)

        self.model_view: Mat4
        self.ui_view: Mat4
        self.update_views()

        self.event("on_resize")(self._on_resize)

    def _init_gl(self, width, height):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        pyglet.gl.glClearColor(0.05, 0, 0.08, 1.0)

        glViewport(0, 0, width, height)

    def update_views(self):
        """
        Updates some internal openGL information, call this whenever the window changes size, or similar
        """
        self.model_view = Mat4.perspective_projection(self.aspect_ratio, z_near=0.01, z_far=50000, fov=Camera.active_camera.FOV)
        self.ui_view = Mat4.orthogonal_projection(0, Window.size.x, 0, Window.size.y, z_near=0, z_far=2555)

    def _on_resize(self, width, height):
        self.screen.width = width
        self.screen.height = height

        Window.size = Vec2(width, height)

        self._init_gl(width, height)
        self.projection = self.ui_view

        self.update_views()

        for entity in Entity.all_entities:
            entity.on_resize()
        
        return pyglet.event.EVENT_HANDLED
