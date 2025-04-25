"""
This module just assists in input handling
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core_ext.collision.collision2D.Hitbox2D import Hitbox2D

from collections import namedtuple
from pyglet.math import Vec2

import pyglet
import typing
import logging

controller_data = namedtuple("ControllerData", ["x", "y"])

class ControllerHandler:
    """
    Passed to pyglet as a controller handler.
    """
    def on_stick_motion(self, controller, stick, vector):
        print(f"stick: {stick} = {vector}")
    
    def on_button_press(self, controller, button_name):
        print(f"pressed {button_name}")

    def on_button_release(self, controller, button_name):
        print(f"released {button_name}")

    def on_trigger_motion(self, controller, trigger, value):
        controller.rumble_play_weak(value, 0.05)
    

class Input:
    """
    Makes it easier to fetch keyboard, mouse, and controller inputs from a centralized class.
    """

    keyboard_keys = pyglet.window.key.KeyStateHandler()

    mouse: Vec2 = Vec2(0, 0)
    mouse_hit_area = Hitbox2D(Vec2(0, 0), Vec2(0, 0), Vec2(0, 0), 0)
    active_mouse_buttons: list[bool] = []

    controller_manager = pyglet.input.ControllerManager()
    controller_handler = ControllerHandler()
    controllers: typing.Dict[int, controller_data] = {}

    def on_mouse_motion(x, y, dx, dy):
        Input.mouse = Vec2(x, y)
        Input.mouse_hit_area.update(Input.mouse, 0)
    
    def on_mouse_press(x, y, button, modifiers):
        Input.active_mouse_buttons.append(button)
        
        Input.mouse = Vec2(x, y)
        Input.mouse_hit_area.update(Input.mouse, 0)

    def on_mouse_release(x, y, button, modifiers):
        if button in Input.active_mouse_buttons:
            Input.active_mouse_buttons.remove(button)
        
        Input.mouse = Vec2(x, y)
        Input.mouse_hit_area.update(Input.mouse, -1)
    
    def on_controller_connect(controller):
        logging.info(f"Controller Connected: {controller}")
        controller.open()
        controller.rumble_play_weak(1.0, 0.1)
        controller.push_handlers(Input.controller_handler)

    def on_controller_disconnect(controller):
        logging.info(f"Controller Disconnected: {controller}")
        controller.remove_handlers(Input.controller_handler)