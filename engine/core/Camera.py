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
import math

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
        logging.debug(f"camera pos: {self.pos}, camera rotation: {self.rotation}")

    def ProjectWorld(self):
        glEnable(GL_DEPTH_TEST)
        self.window.projection = self.window.model_view
        
        # loosely, flip the camera upside down if the player is upside down
        # if this isn't done you get a kind of screen wrapping in first person, very disorienting 
        if self.is_rightside_up():
            self.window.view = Mat4.look_at(position=self.pos, target=self.target, up=Vec3(0, 0, 1))
        else:
            self.window.view = Mat4.look_at(position=self.pos, target=self.target, up=Vec3(0, 0, -1))

    def ProjectHud(self):
        glDisable(GL_DEPTH_TEST)
        self.window.projection = self.window.ui_view
        self.window.view = Mat4()
