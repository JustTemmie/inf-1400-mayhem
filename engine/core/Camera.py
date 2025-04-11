"""
The Camera module contains functions to aid in rendering
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Entity3D import Entity3D

import config

from pyglet.gl import *
from pyglet.math import Mat4, Vec3

import pyglet
import typing
import logging

if typing.TYPE_CHECKING:
    from engine.core.Window import Window


class Camera(Entity3D):
    active_camera = None

    def __init__(self, window: pyglet.window):
        super().__init__()

        self.window: Window = window
        self.visible = False
        self.target: Vec3 = Vec3(0, 0, 0)

        Camera.active_camera = self

        self.pos = Vec3(0, 0, 20)

        self.UI_size = 20
        self.FOV: float = config.FOV

    def engine_process(self, delta):
        logging.debug(f"camera pos: {self.pos}")
        logging.debug(f"camera rotation: {self.rotation}")
        # self.pos += Vec3(3, 0, 0) * delta
        # self.pos += Vec3(0, 0, 4) * delta
        # self.rotation += Vec3(10, 0, 0) * delta

    def ProjectWorld(self):
        glEnable(GL_DEPTH_TEST)
        self.window.projection = self.window.model_view
        self.window.view = Mat4.look_at(position=self.pos, target=self.target, up=Vec3(0, 0, 1))

        # rot_x = Mat4.from_rotation(self.rotation.x, Vec3(1, 0, 0))
        # rot_y = Mat4.from_rotation(self.rotation.y, Vec3(0, 1, 0))
        # rot_z = Mat4.from_rotation(self.rotation.z, Vec3(0, 0, 1))

        # trans = Mat4.from_translation(self.pos)

        # self.window.view = trans @ rot_x @ rot_y @ rot_z

    def ProjectHud(self):
        glDisable(GL_DEPTH_TEST)
        self.window.projection = self.window.ui_view
        self.window.view = Mat4()
