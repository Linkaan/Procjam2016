import abc
from abc import ABCMeta
from abc import abstractproperty

class Entity:
    __metaclass__ = ABCMeta

    def __init__(self, level, x, y):
        self.x = x
        self.y = y
        self.level = level

    @abstractproperty
    def tick(self):
        pass

    @abstractproperty
    def render(self, x_offset, y_offset):
        pass
