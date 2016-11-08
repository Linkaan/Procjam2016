import random
import pygame
import math
from enum import Enum
from entity.entity import Entity
from entity.mob.unit import Unit

class Squad(Entity):

    def __init__(self, level, x, y, unit_count):
        super().__init__(level, x, y)
        self.units = []
        self.unit_count = unit_count
        self.max_speed = math.inf
        self.create_units(x, y)
        self.formation = Formation(self, FormationState.state_broken, self.unit_count, 0)

    def create_units(self, x, y):
        self.axis = random.randint(0, 1)
        for i in range(self.unit_count):
            if self.axis == 0:
                unitx = x
                unity = y - (i - int(self.unit_count / 2) << 5)
            else:
                unitx = x - (i - int(self.unit_count / 2) << 5)
                unity = y
            unit = Unit(self.level, unitx, unity)
            if i == int(self.unit_count / 2):
                self.commander = unit
            self.units.append(unit)
            self.level.add_entity(unit)
            if unit.speed < self.max_speed:
                self.max_speed = unit.speed

    def get_unit_positions(self):
        positions = []
        for unit in self.units:
            positions.append((unit.x, unit.y))
        return positions

    def tick(self):
        '''
        mouse_pos = pygame.mouse.get_pos()
        goal = ((mouse_pos[0] + self.x_offset) >> 5, (mouse_pos[1] + self.y_offset) >> 5)
        has_reached = False
        '''        
        for unit in self.units:
            sum_x = unit.x
            sum_y = unit.y
        self.x = int(sum_x / self.unit_count)
        self.y = int(sum_y / self.unit_count)
        if self.level.updates % 3 == 0:
            self.formation.check_formation(self.x, self.y, self.get_unit_positions())
            self.format_units()



    def distance(self, start, goal):
        return math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

    def render(self, x_offset, y_offset):
        pass

class FormationState(Enum):
    state_broken = 1
    state_forming = 2
    state_formed = 3

class Formation(object):

    def __init__(self, state, unit_count, orientation):
        self.state = state
        self.unit_count = unit_count
        self.orientation = orientation
        self.positions = self.get_formation_positions()

    def get_formation_positions(self):
        positions = []
        for i in range(self.unit_count):
            if self.orientation == 0:
                unitx = 0
                unity = i - int(self.unit_count / 2)
            else:
                unitx = i - int(self.unit_count / 2)
                unity = 0
            positions.append((unitx, unity))
        return positions

    def check_formation(self, x, y, positions):
        if self.state == FormationState.state_forming:
            return
        formation_positions = [(x + pos[0], y + pos[1]) for pos in positions]
        if set(formation_positions) == set(positions):
            self.state = FormationState.state_formed
        else:
            self.state = FormationState.state_broken