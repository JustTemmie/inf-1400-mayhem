# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys
    sys.path.append(".")

from engine.core.Entity3D import Entity3D

import config

from pyglet.gl import glEnable, glDisable, GL_DEPTH_TEST, GL_CULL_FACE
from pyglet.math import Mat4, Vec3

import pyglet
import typing
import logging

if typing.TYPE_CHECKING:
    from engine.core.Window import Window

class Camera(Entity3D):
    def __init__(self, window: pyglet.window):
        super().__init__()
        
        self.window: Window = window
        self.visible = False
        
        self.pos = Vec3(0, 0, 20)
        
        self.UI_size = 20 
        self.FOV: float = config.FOV
    
    def engine_process(self, delta):
        logging.debug(f"camera pos: {self.pos}")
        # self.pos += Vec3(3, 0, 0) * delta
        # self.pos += Vec3(0, 0, 4) * delta
        # self.rotation += Vec3(10, 0, 0) * delta
        print(f"camera rotation: {self.rotation}")
        
        

    def ProjectWorld(self):
        glEnable(GL_DEPTH_TEST)
        self.window.projection = self.window.model_view
        self.window.view = Mat4.look_at(position=self.pos, target=Vec3(0, 0, 0), up=Vec3(0, 1, 0))

    def ProjectHud(self):
        """
            currently unused, may require further testing
        """
        glDisable(GL_DEPTH_TEST)
        self.window.projection = self.window.ui_view
        self.window.view = Mat4.from_translation(Vec3(0, 0, self.UI_size))