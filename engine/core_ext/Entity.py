import pyglet

class Component:
    def __init__(self):
        self.prey = False
        self.flock_with_prey = False

        self.hunter = False
        self.obstacle = False

class Entity:
    time_elapsed: float = 0
    all_entities: list["Entity"] = []

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


    def tick(self, delta):
        print("tick!")
    
    @classmethod
    def get_all_entities(self):
        return self.all_entities