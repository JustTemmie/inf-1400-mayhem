from engine.core.Game import Game
from engine.core_ext.Entity3D import Entity3D

from pyglet.math import Vec3

import pyglet

import typing


class Player(Entity3D):
    def user_init(self):
        print("new ship!")
    
    def tick(self, delta):
        print(f"tickie!! {delta}")
        self.draw()
    
    def user_instantiate(self, game: Game):
        main_batch = game.get_render_batches().main_batch

        model_scene = pyglet.resource.scene("assets/models/test.obj")

        self.model = model_scene.create_models(batch=main_batch)[0]
        
