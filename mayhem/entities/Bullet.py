from engine.core.Entity3D import Entity3D
from engine.core.Game import Game
from engine.core.Utils import Utils

import pyglet


class Bullet(Entity3D):
    def user_init(self):
        self.mass = 0.01
        self.ignore_friction = True

        self.owner = 0

    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("test"))

        self.model = model_scene.create_models(batch=Entity3D.game_object.main_batch)[0]
