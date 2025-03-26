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
game_window = pyglet.window.Window(
    screen_size.x, screen_size.y,
    resizable=True, visible=False,
    caption="Mayhem (3D!!)", vsync=config.VSYNC)

# rendering "batches"
main_batch = pyglet.graphics.Batch()
UI_batch = pyglet.graphics.Batch()

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


@game_window.event
def on_resize(width, height):
    game_window.viewport = (0, 0, width, height)

    game_window.projection = Mat4.perspective_projection(game_window.aspect_ratio, z_near=0.1, z_far=255)
    return pyglet.event.EVENT_HANDLED

class Game:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        example_label = pyglet.text.Label(text="wooho!!", batch=self.get_render_batches().UI_batch)


        self.frames_elapsed: int = 0
        self.time_elapsed: float = 0
        self.frame_times: list[float] = []

        self.entity_ID = 0 # an increasing counter such that every entity has their own unique ID
        self.entities: list[Entity] = []
        self.entities_3D: list[Entity3D] = []

        self.frame_start_time = time.time()


        Utils.print_system_info()

        game_window.view = Mat4.look_at(position=Vec3(0, 0, 5), target=Vec3(0, 0, 0), up=Vec3(0, 1, 0))
        game_window.set_visible()

        self.init()
        
    def init(self):
        """
            Implement by extending class
        """
        pass

    def user_process(self, delta: float):
        """
            Called every frame, implement by extending class
        """
        pass
    
    def user_engine_process(self, delta: float):
        """
            Called every engine tick, implement by extending class
        """
        pass

    def process(self, delta: float):
        """
            Called every frame, not intended to be touched by the end user.
        """
        Entity.time_elapsed = self.time_elapsed
        
        if self.frames_elapsed >= 3:
            self.frame_times.append(delta)
            if len(self.frame_times) > config.target_refresh_rate:
                self.frame_times.pop(0)
        
            fps = 1 / (sum(self.frame_times) / len(self.frame_times))

            # logging.info(f"fps: {round(fps, 1)}, entities: {len(self.entities)}, delta: {round(delta, 6)}, delta*fps: {round(delta * fps, 4)}")
        
        for entity in self.entities:
            entity.process(delta)
        
        # unsure if this is using pointers, might have to fix
        processing_deferred_calls = Entity.deferred_calls
        Entity.deferred_calls = []
        for func in processing_deferred_calls:
            func()
        
        self.frames_elapsed += 1
        self.time_elapsed += delta

    def engine_process(self, delta: float):
        """
            Called every engine tick (30 tps), not intended to be touched by the end user.
        """
        for entity in self.entities:
            entity.engine_process(delta)
        
        # # sort 3D entities' processing order using their Z index to ensure the rendering is done is the correct order
        # self.entities_3D.sort(key=lambda entity: entity.pos.z, reverse=True)

        # # process all loaded 3D entities
        # for entity in self.entities_3D:
        #     entity.tick(delta)
        
        
        self.user_engine_process(delta)
    
    
    def run(self):
        """
            Start the game!
        """
        pyglet.clock.schedule_interval(self.engine_process, 1 / config.target_physics_rate)
        pyglet.clock.schedule_interval(self.process, 1 / config.target_refresh_rate)
        pyglet.app.run()
    
    @staticmethod
    def get_render_batches():
        """
            Get a named tuple of all render batches
        """
        Result = namedtuple("RenderBatches", ["main_batch", "UI_batch"])
        return Result(main_batch, UI_batch)
