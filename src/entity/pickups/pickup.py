import abc
from abc import ABCMeta
from abc import abstractmethod
from entity.entity import Entity

class Pickup(Entity):
    __metaclass__ = ABCMeta

    def __init__(self, level, x, y, sprite):
        super().__init__(level, x, y)
        self.sprite = sprite

    @abstractmethod
    def tick(self):
        # TODO check if a unit picked it up
        pass

    @abstractmethod
    def render(self, surface, x_offset, y_offset):
        self.sprite.render(surface, x_offset, y_offset)
