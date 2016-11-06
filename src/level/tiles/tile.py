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

    def get_id(self):
        return self.tileid

    @abstractproperty
    def tick(self):
        pass

    @abstractproperty
    def render(self, surface, x, y):
        pass
