"""
Blueprint for information shared between 2d and 3d entities
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

import typing
import abc
import logging

if typing.TYPE_CHECKING:
    from engine.core.Game import Game

class Component:
    """
    Different way of storing data for entities, currently unused
    """
    def __init__(self):
        pass


class Entity:
    """
    "Entities", sometimes refered to as "actors", is the parent of any object in the game, everything is an entity.

    Entities are only loaded into the world after their instantiate() function has been called, you may setup other information about them ahead of time.
    """
    # these two really shouldn't be stored in here, but i can't think of a better place to store them
    game_object: "Game"
    time_elapsed: float = 0

    all_entities: list["Entity"] = []

    # list of lambdas to be called at the end of the tick
    deferred_calls: typing.List[typing.Callable] = []

    def __init__(self):
        
        self.entity_ID: int
        self.components = Component()
        self.visible = True

        self.mass = 1  # kg, affects the objects interaction with physics
        self.area = 1  # m^2, affects the objects interaction with air
        self.drag_coeficient = 1
        self.ignore_friction: bool = True
        self.log_spawn: bool = True

        # entities that should also be cleared when this entity is cleared
        self.child_entities: list[Entity] = []

    def on_resize(self):
        """
        Called when the game window is resized
        """
    
    def user_init(self):
        """
        Implement by extending class.
        """

    def process(self, delta):
        """
        Called every frame.
        """

    def engine_process(self, delta):
        """
        Called every engine tick.
        """

    def instantiate(self):
        """
        Instantiates the entity, this adds it to the world, sets their internal entity_ID, and may also load a custom model if the entity has one
        """
        if self.log_spawn:
            logging.info(f"spawning a {self.__class__.__name__}...")

        self.entity_ID = Entity.game_object.entity_ID
        Entity.game_object.entity_ID += 1

        Entity.all_entities.append(self)

        self.user_instantiate()

    def user_instantiate(self):
        """
        Implement by extending class.
        """
        pass
    
    def free(self):
        """
        Frees the object and all children.
        """
        for child in self.child_entities:
            child.free()

        Entity.all_entities.remove(self)

    @classmethod
    def call_deferred(self, call: callable) -> None:
        """
        Deferred calls are called at the end of the frame.
        """
        self.deferred_calls.append(call)
    
    @abc.abstractmethod
    def get_gravity(self):
        """
        Implement by extending class.

        This function is used to get the entity's gravity, it's left as a function so it can easily be overwritten to do anything.
        """
        raise NotImplemented

    @abc.abstractmethod
    def prepare_draw(self, delta):
        """
        This function is called by the engine right before the entity is to be rendered.
        """
        raise NotImplemented

