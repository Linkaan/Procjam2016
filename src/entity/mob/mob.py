import abc
import math
from abc import ABCMeta
from abc import abstractproperty
from entity.entity import Entity

class Mob(Entity):
    __metaclass__ = ABCMeta

    def __init__(self, level, x, y, speed, health):
        super().__init__(level, x, y)
        self.speed = speed
        self.health = health
        self.num_steps = 1
        self.moving_dir = 1
        self.moving = False

    def move(self, xa, ya):
        if xa != 0 and ya != 0:
            self.move(xa, 0)
            self.move(0, ya)
            self.num_steps -= 1
            return

        if ya < 0: self.moving_dir = 0
        if ya > 0: self.moving_dir = 1
        if xa < 0: self.moving_dir = 2
        if xa > 0: self.moving_dir = 3

        while xa != 0:
            axa = self.abs(xa)
            if math.fabs(xa) > 1:
                self.x += axa
                xa -= axa
            else:
                self.x += xa
                xa = 0

        while ya != 0:
            aya = self.abs(ya)
            if math.fabs(ya) > 1:
                self.y += aya
                ya -= aya
            else:
                self.y += ya
                ya = 0
        self.num_steps += 1

    def abs(self, value):
        return -1 if value < 0 else 1

    @abstractproperty
    def tick(self):
        pass

    @abstractproperty
    def render(self, surface, x_offset, y_offset):
        pass
