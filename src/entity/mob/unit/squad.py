import random
import pygame
import math
import heapq
from entity.entity import Entity
from entity.mob.unit.unit import Unit
from level.pathfinding.findpath import find_path
from states.states import FormationState, MovementState, OrderState, UnitPriority

class Squad(Entity):

    squad_id_counter = 0
    def __init__(self, level, x, y, unit_count):
        super().__init__(level, x, y)
        Squad.squad_id_counter += 1
        self.id = Squad.squad_id_counter
        self.units = []
        self.unit_count = unit_count
        self.max_speed = math.inf
        self.create_units(x, y)
        self.formation = Formation(FormationState.state_formed, self.unit_count, self.axis)
        self.cur_forming_unit = None
        self.order_state = OrderState.state_waiting_for_order
        self.goal = None
        self.routes = None
        self.x_offset = 0
        self.y_offset = 0

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
            unit.squad = self
            unit.squad_id = self.id
            if i == int(self.unit_count / 2):
                self.commander = unit
            self.units.append(unit)
            if unit.speed < self.max_speed:
                self.max_speed = unit.speed
        self.level.add_entity(self.commander)
        units_heap = []
        for unit in self.units:
            if unit is self.commander:
                continue
            heapq.heappush(units_heap, (self.distance((unit.x, unit.y), (self.commander.x, self.commander.y)), unit))
        while units_heap:
            self.level.add_entity(heapq.heappop(units_heap)[1])

    def get_unit_positions(self):
        positions = []
        for unit in self.units:
            positions.append((unit.x >> 5, unit.y >> 5))
        return positions

    def get_center_unfilled_pos(self):
        best = None
        for pos in self.formation.positions:
            if self.formation.is_occupied(pos):
                continue
            dist = self.distance(pos, (self.formation.avg_x, self.formation.avg_y))
            if not best or dist < best[0]:
                best = (dist, pos)
        if not best:
            return None
        return best[1]

    def get_unit_for_formattion(self, pos):
        best = None
        for unit in self.units:
            if unit.priority == UnitPriority.state_highest:
                continue
            dist = self.distance(((unit.x - self.x) >> 5, (unit.y - self.y) >> 5), pos)
            if not best or dist < best[0]:
                best = (dist, unit)
        return best[1]

    def format_units(self):
        if not self.formation.state == FormationState.state_forming:
            self.formation.state = FormationState.state_forming
            for unit in self.units:
                unit.priority = UnitPriority.state_lowest
        elif not self.cur_forming_unit or self.cur_forming_unit.movement_state == MovementState.state_reached_goal:
            if self.cur_forming_unit and self.cur_forming_unit.movement_state == MovementState.state_reached_goal:
                print("Setting unit priority to highest")
                self.cur_forming_unit.priority = UnitPriority.state_highest
            formation_pos = self.get_center_unfilled_pos()            
            if not formation_pos:
                print("done forming")
                self.formation.state = FormationState.state_formed
                self.cur_forming_unit = None
                for unit in self.units:
                    unit.priority = UnitPriority.state_medium
                return
            unfilled = ((self.x >> 5) + formation_pos[0], (self.y >> 5) + formation_pos[1])
            self.cur_forming_unit = self.get_unit_for_formattion(unfilled)
            self.cur_forming_unit.goto(unfilled)
            self.formation.set_occupied(formation_pos, self.cur_forming_unit)

    def get_possible_goals(self):
        goals = {}
        goals[self.commander] = self.goal
        for unit, pos in zip(self.units, self.formation.positions):
            if unit is self.commander:
                continue
            goals[unit] = (self.goal[0] + pos[0], self.goal[1] + pos[1])
        return goals
        
    def get_valid_routes(self):
        goals = self.get_possible_goals()
        commander_goal = goals.get(self.commander)
        assert commander_goal
        routes = {}
        routes[self.commander] = {"goal": commander_goal, "path": find_path(self.level, self.commander.start, commander_goal, self.id)}
        route = routes[self.commander]["path"][:]
        route.reverse()
        for unit in self.units:
            if unit is self.commander:
                continue
            dx = abs(unit.start[0] - self.commander.start[0])
            dy = abs(unit.start[1] - self.commander.start[1])
            goal = goals.get(unit)
            new_route = []
            if goal[0] < commander_goal[0]:
                dx = -dx
            if goal[1] < commander_goal[1]:
                dy = -dy
            print(str(dy) + " when goal is " + str(goal))
            for move in route:
                new_move = (move[0] + dx , move[1] + dy)
                new_route.append(new_move)
                #if new_move == goal:
                #    break
            new_route.reverse()            
            #assert goal == new_route[0]
            routes[unit] = {"goal": goal, "path": new_route}
        return routes

    def follow_closet_centered_unit(self, follower_unit):
        print("following unit is " + str(follower_unit.id))
        # stall all other units and find closest
        closest = None
        for unit in self.units:
            if unit is follower_unit:
                continue
            #unit.movement_state = MovementState.state_stalling
            dist = self.distance((follower_unit.x, follower_unit.y), (unit.x, unit.y))
            commander_dist = self.distance((unit.x, unit.y), (self.commander.x, self.commander.y))
            if not closest or dist < closest[1] and commander_dist < closest[2]:
                closest = [unit, dist, commander_dist]
        assert closest
        return closest[0].last_start

    def tick(self):
        if self.level.game.mouse_up:
            mouse_pos = pygame.mouse.get_pos()            
            self.goal = ((mouse_pos[0] + self.x_offset) >> 5, (mouse_pos[1] + self.y_offset) >> 5)
            self.order_state = OrderState.state_waiting_for_target
            print("Target selected: ", end="")
            print(self.goal)
        #if self.level.updates % 45:
        #    self.formation.set_orientation(random.randint(0, 1))
        sum_x = 0
        sum_y = 0
        for unit in self.units:
            sum_x += unit.x
            sum_y += unit.y
        self.x = int(sum_x / self.unit_count)
        self.y = int(sum_y / self.unit_count)
        if self.level.updates % 3 == 0:
            self.formation.check_formation(self.x>>5, self.y>>5, self.get_unit_positions())
        #if self.formation.state != FormationState.state_formed:
        #    self.format_units()
        elif self.order_state == OrderState.state_waiting_for_target:            
            # calculate goals for each unit
            # calculate routes for each unit to move based on commander unit position
            self.routes = self.get_valid_routes()
            if not self.routes:
                self.order_state = OrderState.state_waiting_for_order
            else:
                self.order_state = OrderState.state_moving_to_target
                for unit in self.units:
                    route = self.routes.get(unit)
                    assert route
                    print(route)
                    unit.goal = route["goal"]
                    unit.path = route["path"]
                    unit.movement_state = MovementState.state_moving
        elif self.order_state == OrderState.state_moving_to_target:
            print("we are moving to target")
            moving = True
            # check if all units are moving (exception if units have reached the goal)
            for unit in self.units:
                if unit.movement_state == MovementState.state_waiting_for_path:
                    moving = False
                    break
            # if not then we try to change orientation of formation and recalculate route
            #f not moving:
            #    self.formation.set_orientation(0 if self.formation.orientation == 1 else 1)
            #    self.order_state = OrderState.state_waiting_for_target
        if self.order_state == OrderState.state_moving_to_target and self.commander.movement_state == MovementState.state_reached_goal:
            print("Reached destination")
            self.order_state = OrderState.state_waiting_for_order        

    def distance(self, start, goal):
        return math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

    def render(self, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset

class Formation(object):

    def __init__(self, state, unit_count, orientation):
        self.state = state
        self.unit_count = unit_count
        self.set_orientation(orientation)

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

    def set_orientation(self, orientation):
        self.orientation = orientation
        self.positions = self.get_formation_positions()
        self.filled = None

    def check_formation(self, x, y, positions):
        if self.state == FormationState.state_forming:
            return
        position_offset = 1 if self.unit_count % 2 == 0 else 0
        if self.orientation == 0:
            x_offset = 0
            y_offset = position_offset
        else:
            x_offset = position_offset
            y_offset = 0
        formation_positions = [(x + pos[0] + x_offset, y + pos[1] + y_offset) for pos in self.positions]
        if set(formation_positions) == set(positions):
            self.state = FormationState.state_formed
        else:
            print(formation_positions, end="")
            print(" and ", end="")
            print(positions)
            self.state = FormationState.state_broken
            self.filled = None

    def set_occupied(self, pos, unit):
        if not self.filled:
            self.filled = {}
        self.filled[pos] = unit

    def get_occupied(self, pos):
        if not self.filled:
            return None
        else:
            return self.filled.get(pos)

    def is_occupied(self, pos):
        if self.filled:
            return pos in self.filled
        else:
            return False
