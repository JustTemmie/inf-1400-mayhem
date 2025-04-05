import pyglet
import typing
import abc

if typing.TYPE_CHECKING:
    from engine.core.Game import Game

class Component:
    def __init__(self):
        pass

class Entity:
    time_elapsed: float = 0
    all_entities: list["Entity"] = []

    # list of lambdas to be called at the end of the tick
    deferred_calls: typing.List[typing.Callable] = []

    def __init__(self):
        self.entity_ID: int
        self.components = Component()
        self.visible = True
        
        self.mass = 1 # kg

        # entities that should also be cleared when this entity is cleared
        self.child_entities: list[Entity] = []
    
    def user_init(self):
        """
            Implement by extending class
        """
        pass

    def process(self, delta):
        """
            Called every frame
        """

    def engine_process(self, delta):
        """
            Called every engine tick
        """

    def instantiate(self, game):
        game: Game = game
        
        self.entity_ID = game.entity_ID
        game.entity_ID += 1

        Entity.all_entities.append(self)

        self.user_instantiate(game)

    def user_instantiate(self, game):
        """
            Implement by extending class
        """
        
        game: Game = game

    @abc.abstractmethod
    def prepare_draw(self, delta):
        raise NotImplemented

    @classmethod
    def get_all_entities(self) -> list["Entity"]:
        return self.all_entities

    @classmethod
    def call_deferred(self, call: callable) -> None:
        self.deferred_calls.append(call)