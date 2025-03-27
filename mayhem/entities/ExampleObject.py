from engine.core.Game import Game
from engine.core.Utils import Utils
from engine.core.Entity3D import Entity3D

import pyglet


class ExampleObject(Entity3D):
    def user_instantiate(self, game: Game):
        model_scene = pyglet.resource.scene(Utils.get_model_path("test"))

        self.model = model_scene.create_models(batch=game.main_batch)[0]
