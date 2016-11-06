import abc
from abc import ABCMeta
from abc import abstractproperty

class Tile:
    __metaclass__ = ABCMeta

    tiles = [None]*256

    def __init__(self, tileid, is_solid):
        self.tileid = tileid
        assert self.tiles[tileid] == None
        self.solid = is_solid
        self.tiles[tileid] = self

    def getId(self):
        return self.tileid

    @abstractproperty
    def tick(self):
        pass

    @abstractproperty
    def render(self, level, surface, x, y):
        pass
