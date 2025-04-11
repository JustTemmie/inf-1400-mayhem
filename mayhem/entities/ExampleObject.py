"""
The minimum required to create a 3D object.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Utils import Utils
from engine.core.Entity3D import Entity3D

import pyglet


class ExampleObject(Entity3D):
    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("test"))

        self.model = model_scene.create_models(batch=Entity3D.game_object.main_batch)[0]
