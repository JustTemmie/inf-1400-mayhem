# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys

    sys.path.append(".")

from engine.core.Camera import Camera

import config

from pyglet.gl import *
from pyglet.math import Mat4, Vec3, Vec2

import pyglet


# a lot of this code is from https://stackoverflow.com/q/72074133
class Window(pyglet.window.Window):
    size: Vec2 = config.display_resolution

    def __init__(self):
        gl_config = Config(
            sample_buffers=1, samples=4, depth_size=16, double_buffer=True
        )

        super().__init__(
            Window.size.x,
            Window.size.y,
            resizable=True,
            visible=False,
            config=gl_config,
            vsync=config.VSYNC,
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
        # glEnable(GL_LIGHTING)

        # glLightfv(GL_LIGHT0, GL_SPECULAR, (GLfloat*4)(.5,.5,1,1))
        # glLightfv(GL_LIGHT0, GL_DIFFUSE,  (GLfloat*4)(1,1,1,1))
        # glLightfv(GL_LIGHT0, GL_POSITION, (GLfloat*4)(1, 0, .5, 0))
        # glEnable(GL_LIGHT0)

        # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # glEnable(GL_TEXTURE_2D)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # sky colour :3
        pyglet.gl.glClearColor(0.6, 0.75, 0.92, 1.0)

        glViewport(0, 0, width, height)

    def update_views(self):
        self.model_view = Mat4.perspective_projection(
            self.aspect_ratio, z_near=0.01, z_far=400, fov=Camera.active_camera.FOV
        )
        self.ui_view = Mat4.orthogonal_projection(
            0, Window.size.x, 0, Window.size.y, z_near=0, z_far=2555
        )

    def _on_resize(self, width, height):
        self.screen.width = width
        self.screen.height = height

        Window.size = Vec2(width, height)

        self._init_gl(width, height)
        self.projection = self.ui_view

        self.update_views()

        return pyglet.event.EVENT_HANDLED
