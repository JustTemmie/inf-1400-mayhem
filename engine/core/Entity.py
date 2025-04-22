"""
Blueprint for information shared between 2d and 3d entities ( write more later )
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

import typing
import abc

if typing.TYPE_CHECKING:
    from engine.core.Game import Game


class Component:
    def __init__(self):
        pass


class Entity:
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

        # entities that should also be cleared when this entity is cleared
        self.child_entities: list[Entity] = []

    def on_resize(self):
        """
        Called when the game window is resized
        """
        pass
    
    def user_init(self):
        """
        Implement by extending class.
        """
        pass

    def process(self, delta):
        """
        Called every frame.
        """

    def engine_process(self, delta):
        """
        Called every engine tick.
        """

    def instantiate(self):
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

    @abc.abstractmethod
    def prepare_draw(self, delta):
        """
        Implement by extending class.
        This function is called by the engine right before the entity is to be rendered.
        """
        raise NotImplemented

    @classmethod
    def call_deferred(self, call: callable) -> None:
        """
        Deferred calls are called at the end of the frame.
        """
        self.deferred_calls.append(call)
