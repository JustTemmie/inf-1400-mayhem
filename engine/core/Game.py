# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys
    sys.path.append(".")

# from engine.core.Input import Input
from engine.core.Utils import Utils
from engine.core.Window import Window
from engine.core_ext.Input import Input
from engine.core.Entity import Entity
from engine.core.Entity3D import Entity3D
import engine.extras.logger

import config

from collections import namedtuple

import pyglet
import sys
import typing
import time
import logging

class Game:
    def __init__(self):
        # rendering "batches"
        self.main_batch = pyglet.graphics.Batch()
        self.UI_batch = pyglet.graphics.Batch()
        
        
        self.window = Window()
        self.window.event("on_draw")(self.on_draw)
        self.window.event("on_mouse_motion")(Input.on_mouse_motion)
        self.window.push_handlers(Input.keyboard_keys)

        example_label = pyglet.text.Label(text="wooho!!", batch=self.UI_batch)

        self.frames_elapsed: int = 0
        self.time_elapsed: float = 0
        self.frame_times: list[float] = []

        self.entity_ID = 0 # an increasing counter such that every entity has their own unique ID

        self.frame_start_time = time.time()

        Utils.print_system_info()

        self.init()
        self.window.camera.instantiate(self)
        self.window.set_visible()

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

            logging.info(f"fps: {round(fps, 1)}, entities: {len(Entity.all_entities)}, delta: {round(delta, 6)}, delta*fps: {round(delta * fps, 4)}")

        for entity in Entity.all_entities:
            entity.process(delta)
            
        
        for entity in Entity.all_entities:
            if entity.visible:
                entity.draw()

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
        for entity in Entity.all_entities:
            entity.engine_process(delta)
        
        for entity in Entity3D.all_3D_entities:
            entity.handle_physics(delta, air_friction=config.air_friction, gravity=config.gravity)

        # # sort 3D entities' processing order using their Z index to ensure the rendering is done is the correct order
        # self.entities_3D.sort(key=lambda entity: entity.pos.z, reverse=True)

        # # process all loaded 3D entities
        # for entity in self.entities_3D:
        #     entity.tick(delta)


        self.user_engine_process(delta)

    def on_draw(self):
        self.window.clear()

        self.window.camera.ProjectWorld()
        
        self.main_batch.draw()
        self.UI_batch.draw()
    
    def run(self):
        """
            Start the game!
        """
        pyglet.clock.schedule_interval(self.engine_process, 1 / config.target_physics_rate)
        pyglet.clock.schedule_interval(self.process, 1 / config.target_refresh_rate)
        pyglet.app.run()