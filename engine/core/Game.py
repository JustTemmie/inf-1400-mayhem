"""
Main module. ( write more later )
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

# core modules are simply defined as what is imported by this file
from engine.extras.Utils import Utils
from engine.core.Camera import Camera
from engine.core.Window import Window
from engine.core.Input import Input
from engine.core.Entity import Entity
from engine.core.Entity2D import Entity2D
from engine.core.Entity3D import Entity3D

from engine.core.Music import MusicManager

import config

import pyglet
import time
import logging

class Game:
    """
    Contains the game loop itself, this is what you want to extend if you're making a game.

    the class' init() function is called when the engine is ready to do anything, use this over __init__().
    """

    def __init__(self):
        Utils.print_system_info()
        if config.PLAY_SFX:
            pyglet.options["audio"] = ("directsound")

        # rendering "batches"
        self.main_batch = pyglet.graphics.Batch()
        self.UI_batch = pyglet.graphics.Batch()

        if config.PLAY_MUSIC:
            self.music_manager = MusicManager()
        
        self.window = Window()
        self.window.event("on_draw")(self.on_draw)
        self.window.event("on_mouse_motion")(Input.on_mouse_motion)
        self.window.event("on_mouse_press")(Input.on_mouse_press)
        self.window.event("on_mouse_release")(Input.on_mouse_release)
        self.window.push_handlers(Input.keyboard_keys)
        self.window.push_handlers(Input.controller_manager)


        self.frames_elapsed: int = 0
        self.time_elapsed: float = 0
        self.frame_times: list[float] = []

        self.entity_ID = 0  # an increasing counter such that every entity has their own unique ID
        self.frame_start_time = time.time()

        Entity.game_object = self

        Camera.active_camera.instantiate()

        Input.controller_manager.on_connect = Input.on_controller_connect
        Input.controller_manager.on_disconnect = Input.on_controller_disconnect
        # handle already connected controllers
        if controllers := Input.controller_manager.get_controllers():
            for controller in controllers:
                Input.on_controller_connect(controller)

        self.init()

        self.window.set_visible()

    def init(self):
        """
        Called when the game is started.
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
        Called every frame (60 fps by default).

        Not intended to be touched by the end user, instead use user_process()
        """
        Entity.time_elapsed = self.time_elapsed

        if self.frames_elapsed >= 3:
            self.frame_times.append(delta)
            if len(self.frame_times) > config.target_refresh_rate:
                self.frame_times.pop(0)

            fps = 1 / (sum(self.frame_times) / len(self.frame_times))

            logging.debug(f"fps: {round(fps, 1)}, entities: {len(Entity.all_entities)}, delta: {round(delta, 6)}, delta*fps: {round(delta * fps, 4)}")
            
            if fps * 1.2 < config.target_refresh_rate:
                logging.warning(f"the current fps of {round(fps, 1)} is a lot lower than the target fps of {config.target_refresh_rate}, this can lead to choppy feeling behaviour")

        for entity in Entity.all_entities:
            entity.process(delta)

        for entity in Entity.all_entities:
            if entity.visible:
                entity.prepare_draw(delta)

        # unsure if this is using pointers, might have to fix
        processing_deferred_calls = Entity.deferred_calls
        Entity.deferred_calls = []
        for func in processing_deferred_calls:
            func()

        self.frames_elapsed += 1
        self.time_elapsed += delta

    def engine_process(self, delta: float):
        """
        Called every engine tick (60 tps by default).

        Not intended to be touched by the end user, instead use user_engine_process()
        """
        for entity in Entity.all_entities:
            entity.engine_process(delta)
        
        self.user_engine_process(delta)

        for entity in Entity2D.all_2D_entities:
            entity.handle_physics(delta, air_friction=config.air_friction)

        for entity in Entity3D.all_3D_entities:
            entity.handle_physics(delta, air_friction=config.air_friction)

        # using deltas here could crash the game due to audio players potentially having negative volume
        if config.PLAY_MUSIC:
            self.music_manager.process_fading()
    
    def on_draw(self):
        """
        Called every time pyglet attempts to render a frame.

        You probably shouldn't be calling this manually.
        """
        self.window.clear()

        Camera.active_camera.ProjectWorld()
        self.main_batch.draw()

        Camera.active_camera.ProjectHud()
        self.UI_batch.draw()

    def run(self):
        """
        Start the game!
        """
        pyglet.clock.schedule_interval(self.engine_process, 1 / config.target_physics_rate)
        pyglet.clock.schedule_interval(self.process, 1 / config.target_refresh_rate)
        pyglet.app.run()
