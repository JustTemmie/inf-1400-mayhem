import pyglet
import typing

class Component:
    def __init__(self):
        self.prey = False
        self.flock_with_prey = False

        self.hunter = False
        self.obstacle = False

class Entity:
    time_elapsed: float = 0
    all_entities: list["Entity"] = []

    # list of lambdas to be called at the end of the tick
    deferred_calls: typing.List[typing.Callable] = []

    def __init__(self):
        self.entity_ID: int
        self.components = Component()

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
        print("tick!")
    
    def engine_process(self, delta):
        """
            Called every engine tick
        """
    
    @classmethod
    def get_all_entities(self) -> list["Entity"]:
        return self.all_entities

    @classmethod
    def call_deferred(self, call: callable) -> None:
        self.deferred_calls.append(call)