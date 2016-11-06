import pygame
from GameConfig import *
from level.tiles.tiles import *
from level.tiles.tile import Tile
from level.tiles.map import Tilemap

class Level(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.entities = []
        self.tilemap = Tilemap(self, self.width, self.height)
        self.x_offset = 0
        self.y_offset = 0

    def add_entity(self, entity):
        self.entities.append(entity)
        print(entity)

    def tick(self):
        for tile in Tile.tiles:
            if not tile:
                break
            tile.tick()
        for entity in self.entities:
            entity.tick()

    def render(self, surface, x_offset, y_offset):
        from graphics.textures import Textures
        if x_offset < 0:
            x_offset = 0
        if x_offset > ((self.width << 5) - SCREEN_SIZE[0]):
            x_offset = ((self.width << 5) - SCREEN_SIZE[0])
        if y_offset < 0:
            y_offset = 0
        if y_offset > ((self.height << 5) - SCREEN_SIZE[1]):
            y_offset = ((self.height << 5) - SCREEN_SIZE[1])

        self.x_offset = x_offset;
        self.y_offset = y_offset;

        for y in range(y_offset >> 5, (y_offset + SCREEN_SIZE[1] >> 5) + 1):
            for x in range(x_offset >> 5, (x_offset + SCREEN_SIZE[0] >> 5) + 1):
                if 0 > x or x >= self.width or 0 > y or y >= self.height:
                    continue
                Tile.tiles[self.tilemap.map[x + y * self.width]].render(surface, (x << 5) - x_offset, (y << 5) - y_offset)

        for entity in self.entities:
            # TODO ignore entities not on screen
            entity.render(surface, x_offset, y_offset)

    def get_tile(self, x, y):
        if 0 > x or x >= self.width or 0 > y or y >= self.height:
            return VOID
        return Tile.tiles[self.tilemap.map[x + y * self.width]]
