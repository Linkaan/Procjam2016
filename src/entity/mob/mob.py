import abc
import math
from abc import ABCMeta
from abc import abstractproperty
from entity.entity import Entity

class Mob(Entity):
    __metaclass__ = ABCMeta

    mob_id_counter = 0
    def __init__(self, level, x, y, speed, health):
        super().__init__(level, x, y)
        Mob.mob_id_counter += 1
        self.id = Mob.mob_id_counter
        self.speed = speed
        self.health = health
        self.moving_dir = 1

    def move(self, xa, ya):
        if xa != 0 and ya != 0:
            self.move(xa, 0)
            self.move(0, ya)
            return

        if not self.has_collided(xa, ya):
            if ya < 0: self.moving_dir = 0
            if ya > 0: self.moving_dir = 1
            if xa < 0: self.moving_dir = 2
            if xa > 0: self.moving_dir = 3

            while xa != 0:
                axa = self.abs(xa)
                if math.fabs(xa) > 1:
                    if not self.has_collided(axa, ya):
                        self.x += axa
                    xa -= axa
                else:
                    if not self.has_collided(axa, ya):
                        self.x += xa
                    xa = 0
            while ya != 0:
                aya = self.abs(ya)
                if math.fabs(ya) > 1:
                    if not self.has_collided(xa, aya):
                        self.y += aya
                    ya -= aya
                else:
                    if not self.has_collided(xa, aya):
                        self.y += ya
                    ya = 0
        else:
            return False
        return True

    def __lt__(self, other):
        return self.id < other.id

    def abs(self, value):
        return -1 if value < 0 else 1

    @abstractproperty
    def has_collided(self, xa, ya):
        pass

    @abstractproperty
    def tick(self):
        pass

    @abstractproperty
    def render(self, x_offset, y_offset):
        pass
