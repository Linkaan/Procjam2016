import pygame
import numpy as np
import random
from GameConfig import *
from level.tiles.tiles import *
from level.bsp.leaf import Leaf
from entity.pickups.bazooka_pickup import BazookaPickup
from entity.mob.squad import Squad

class Tilemap(object):

    def __init__(self, level, width, height):
        self.level = level
        self.width = width
        self.height = height
        self.map = np.ndarray((self.width*self.height,),int)
        self.generate_map()

    def print_level(self):
        with open("level.dat", "w") as f:
            f.write("RNG SEED USED: " + self.level.seed + "\n")
            for y in range(self.height):
                for x in range(self.width):
                    tile_id = self.map[x + y * self.width]
                    if tile_id == WALL.get_id():
                        f.write("###")
                    elif tile_id == ROAD.get_id():
                        f.write("   ")
                f.write("\n")

    def carve_level(self, leafs):
        for l in leafs:
            if l.halls:
                for r in l.halls:
                    for y in range(r.y1, r.y2):
                        for x in range(r.x1, r.x2):
                            self.map[x + y * self.width] = ROAD.get_id()
            if l.room:
                for y in range(l.room.y1, l.room.y2):
                    for x in range(l.room.x1, l.room.x2):
                        self.map[x + y * self.width] = ROAD.get_id()

    def populate_room(self, leafs, biggest):
        for l in leafs:
            if l.room:
                if biggest.room.intersects(l.room):
                    self.level.add_entity(Squad(self.level, l.room.center[0] << 5, l.room.center[1] << 5, 3))
                    continue
                self.level.add_entity(BazookaPickup(self.level, l.room.center[0] << 5, l.room.center[1] << 5))

    def generate_map(self):
        for y in range(self.height):
            for x in range(self.width):
                self.map[x + y * self.width] = WALL.get_id()
        leafs = []

        root = Leaf(0, 0, self.width, self.height)
        leafs.append(root)

        did_split = True
        biggest = None

        while did_split:
            did_split = False
            _leafs = leafs[:]
            for l in _leafs:
                assert l
                if l.left_child is None and l.right_child is None:
                    if l.width > MAX_LEAF_SIZE or l.height > MAX_LEAF_SIZE or random.random() < 0.75:
                        if l.split():
                            assert l.left_child
                            assert l.right_child
                            leafs.append(l.left_child)
                            leafs.append(l.right_child)
                            if l.width <= MAX_LEAF_SIZE and l.height <= MAX_LEAF_SIZE and 0.8 <= l.width / l.height <= 1.25 and (biggest is None or l.width*l.height > biggest.width*biggest.height):
                                biggest = l
                            did_split = True
        assert biggest
        biggest.create_room(True)
        root.create_rooms()
        self.populate_room(leafs, biggest)
        self.carve_level(leafs)
        self.print_level()
