import sys
import random
import base64
import pygame
from GameConfig import *
from level.tiles.tiles import *
from level.tiles.tile import Tile
from level.tiles.map import Tilemap

class Level(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sprite_group = pygame.sprite.Group()
        self.entities = []
        self.seed = "MjY4NzQ3MDYzODcyODcwMzY4NA=="#base64.b64encode(str(random.randint(0, sys.maxsize)).encode('ascii')).decode('ascii')
        random.seed(self.seed)
        self.tilemap = Tilemap(self, self.width, self.height)
        self.graph = {}
        self.x_offset = 0
        self.y_offset = 0
        self.build_graph()

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
            entity.render(x_offset, y_offset)

        for sprite in self.sprite_group:
            if sprite.render_flag:
                surface.blit(sprite.image, sprite.rect)
                pygame.draw.rect(surface, (255, 0, 255), sprite.posrect, 2)
            sprite.render_flag = False

    def build_graph(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if not Tile.tiles[self.tilemap.map[x + y * self.width]].solid:
                    for i in range(8):
                        xi = (i % 3) - 1
                        yi = int(i / 3) - 1
                        a = (x + xi, y + yi)
                        at = self.get_tile(a[0], a[1])
                        if not at.solid:
                            arr = self.graph.get((x, y))
                            if not arr:
                                arr = set()
                            arr.add(a)
                            self.graph[(x, y)] = arr
        #print(self.graph[(20, 25)])

    def get_tile(self, x, y):
        assert isinstance(x, int) and isinstance(y, int)
        if 0 > x or x >= self.width or 0 > y or y >= self.height:
            return VOID
        return Tile.tiles[self.tilemap.map[x + y * self.width]]
