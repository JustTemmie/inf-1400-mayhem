# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys
    sys.path.append(".")

# from engine.core.Input import Input
from engine.core.Utils import Utils
from engine.core_ext.Entity import Entity
import engine.extras.logger

import config

from collections import namedtuple
from pyglet.gl import glEnable, GL_DEPTH_TEST, GL_CULL_FACE
from pyglet.math import Mat4, Vec3


import pyglet
import sys
import typing
import time
import logging


if typing.TYPE_CHECKING:
    from engine.core_ext.Entity import Entity
    from engine.core_ext.Entity3D import Entity3D


screen_size = config.display_resolution
game_window = pyglet.window.Window(screen_size.x, screen_size.y, resizable=True)
main_batch = pyglet.graphics.Batch()

@game_window.event
def on_resize(width, height):
    game_window.viewport = (0, 0, width, height)

    game_window.projection = Mat4.perspective_projection(game_window.aspect_ratio, z_near=0.1, z_far=255)
    return pyglet.event.EVENT_HANDLED

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

class Game:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)


        example_label = pyglet.text.Label(text="wooho!!", batch=main_batch)

        # pygame.display.set_caption("Mayhem (3D!!)")

        self.frames_elapsed: int = 0
        self.time_elapsed: float = 0
        self.frame_times: list[float] = []

        self.entity_ID = 0 # an increasing counter such that every entity has their own unique ID
        self.entities: list[Entity] = []
        self.entities_3D: list[Entity3D] = []

        # list of lambdas to be called at the end of the tick
        self.deferred_calls: typing.List[typing.Callable] = []

        # self.clock = pygame.time.Clock()
        self.frame_start_time = time.time()


        Utils.print_system_info()
        pyglet.clock.schedule_interval(self.engine_tick, 1 / config.target_refresh_rate)

        game_window.view = Mat4.look_at(position=Vec3(0, 0, 5), target=Vec3(0, 0, 0), up=Vec3(0, 1, 0))

        self.init()
        
    def init(self):
        """
            Implement by extending class
        """
        pass

    def tick(self, delta: float):
        """
            Implement by extending class
        """
        pass

    def engine_tick(self, delta: float):
        Entity.time_elapsed = self.time_elapsed

        for entity in self.entities:
            entity.tick(delta)
        
        # # sort 3D entities' processing order using their Z index to ensure the rendering is done is the correct order
        # self.entities_3D.sort(key=lambda entity: entity.pos.z, reverse=True)

        # # process all loaded 3D entities
        # for entity in self.entities_3D:
        #     entity.tick(delta)
        
        # process all deferred calls
        processing_deferred_calls = self.deferred_calls
        self.deferred_calls = []
        for func in processing_deferred_calls:
            func()
        
        self.tick(delta)

        self.frames_elapsed += 1
        self.time_elapsed += delta
    
    def run(self):
        pyglet.app.run()
    
    @staticmethod
    def get_render_batches():
        Result = namedtuple("RenderBatches", ["main_batch"])
        return Result(main_batch)