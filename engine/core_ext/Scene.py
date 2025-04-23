"""
Contains the Scene class

authors: BAaboe (Change later)
"""
from engine.core.Entity import Entity
from engine.core.Entity2D import Entity2D
from engine.core.Entity3D import Entity3D

import logging


class Scene:
    """
    This may be a to big change two days before hand in.
    """
    def __init__(self):
        self.entities = {}

    def add_entity(self, entity_ptr, **kwargs):
        self.entities[entity_ptr] = kwargs

    @classmethod
    def set_scene(scene: "Scene"):
        for entity in Entity2D.all_2D_entities:
            entity.free()

        for entity in Entity3D.all_3D_entities:
            entity.free()

        for entity_ptr, args in scene.entities:
            entity = entity_ptr()
            for attr, value in args:
                if hasattr(entity, attr):
                    setattr(entity, attr, value)
                else:
                    logging.warn(f'Class "{type(entity).__name__}" has no attribute "{attr}"')
            entity.instantiate()
