import random
import pygame
import math
from entity.entity import Entity
from entity.mob.unit import Unit

class Squad(Entity):

    def __init__(self, level, x, y, unit_count):
        super().__init__(level, x, y)
        self.units = []
        self.unit_count = unit_count
        self.create_units(x, y)
        self.x_offset = 0
        self.y_offset = 0

    def create_units(self, x, y):
        axis = random.randint(0, 1)
        for i in range(self.unit_count):
            if axis == 0:
                unitx = x
                unity = y - (i - int(self.unit_count / 2) << 5)
            else:
                unitx = x - (i - int(self.unit_count / 2) << 5)
                unity = y
            self.units.append(Unit(self.level, unitx, unity))
            self.level.add_entity(self.units[-1])

    def tick(self):
        mouse_pos = pygame.mouse.get_pos()
        goal = ((mouse_pos[0] + self.x_offset) >> 5, (mouse_pos[1] + self.y_offset) >> 5)
        has_reached = False
        for unit in self.units:
            if unit.start == goal:
                has_reached = True
            else:
                unit.goal = goal
            sum_x = unit.x
            sum_y = unit.y
        if has_reached:
            for unit in self.units:
                unit.path = None
        self.x = int(sum_x / self.unit_count)
        self.y = int(sum_y / self.unit_count)

    def distance(self, start, goal):
        return math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

    def render(self, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset
