import random
import pygame
import math
from entity.entity import Entity
from entity.mob.unit.unit import Unit
from states.states import FormationState, MovementState

class Squad(Entity):

    def __init__(self, level, x, y, unit_count):
        super().__init__(level, x, y)
        self.units = []
        self.unit_count = unit_count
        self.max_speed = math.inf
        self.create_units(x, y)
        self.formation = Formation(self, FormationState.state_broken, self.unit_count, 0)
        self.cur_forming_unit = None

    def create_units(self, x, y):
        self.axis = random.randint(0, 1)
        for i in range(self.unit_count):
            if self.axis == 0:
                unitx = x
                unity = y - (i - int(self.unit_count / 2) << 5)
            else:
                unitx = x - (i - int(self.unit_count / 2) << 5)
                unity = y
            unit = Unit(self, self.level, unitx, unity)
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


    def get_center_unfilled_pos(self):
        best = None
        for pos in self.formation.positions:
            if self.formation.is_occupied(pos):
                continue
            dist = self.distance(pos, (self.formation.avg_x, self.formation.avg_y))
            if not best or dist < best[0]:
                best = (dist, pos)
        self.formation.set_occupied(best[1])
        return best[1]

    def get_unit_for_formattion(self, pos):
        best = None
        for unit in self.units:
            dist = self.distance((unit.x - self.x, unit.y - self.y), pos)
            if not best or dist < best[0]:
                best = (dist, unit)
        return best



    '''
    Set all units' internal group movement priorities to same low priority value.
    Set state to cStateForming.
    While state is cStateForming:
    {
    Find the unfilled position that's closest to the center of the formation.
    If no unit was available
    Set the state to cStateFormed and break out of forming loop.

    Select a unit to fill that slot using a game specific heuristic that:
    Minimizes the distance the unit has to travel.
    Will collide with the fewest number of other formation members.
    Has the lowest overall travel time.

    Set unit's movement priority to a medium priority value.
    Wait (across multiple game updates) until unit is in position.
    Set unit's movement priority to highest possible value. This ensures that
    subsequently formed units will not dislodge this unit.
    }
    '''
    def format_units(self):
        if not self.formation.state == FormationState.state_forming:
            self.formation.state = FormationState.state_forming
        elif not self.cur_forming_unit or self.cur_forming_unit.movement_state == MovementState.state_reached_goal:
            unfilled = self.get_center_unfilled_pos()
            if not unfilled:
                self.formation.state = FormationState.state_forming
                self.cur_forming_unit = None
                return
            self.cur_forming_unit = self.get_unit_for_formattion(unfilled)


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
        if self.formation.state != FormationState.state_formed:
            self.format_units()



    def distance(self, start, goal):
        return math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

    def render(self, x_offset, y_offset):
        pass

class Formation(object):

    def __init__(self, state, unit_count, orientation):
        self.state = state
        self.unit_count = unit_count
        self.orientation = orientation
        self.positions = self.get_formation_positions()
        self.filled = None

    def get_formation_positions(self):
        positions = []
        self.avg_x = 0
        self.avg_y = 0
        for i in range(self.unit_count):
            if self.orientation == 0:
                unitx = 0
                unity = i - int(self.unit_count / 2)
            else:
                unitx = i - int(self.unit_count / 2)
                unity = 0
            self.avg_x += unitx
            self.avg_y += unitx
            positions.append((unitx, unity))
        self.avg_x /= self.unit_count
        self.avg_y /= self.unit_count
        return positions

    def check_formation(self, x, y, positions):
        if self.state == FormationState.state_forming:
            return
        formation_positions = [(x + pos[0], y + pos[1]) for pos in positions]
        if set(formation_positions) == set(positions):
            self.state = FormationState.state_formed
        else:
            self.state = FormationState.state_broken
            self.filled = None

    def set_occupied(self, pos):
        if not self.filled:
            self.filled = set()
        self.filled.add(pos)

    def is_occupied(self, pos):
        if self.filled:
            return pos in self.filled
        else:
            return False