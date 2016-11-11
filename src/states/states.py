from enum import Enum

class FormationState(Enum):
    state_broken = 1
    state_forming = 2
    state_formed = 3

class MovementState(Enum):
    state_moving = 1
    state_reached_goal = 2
    state_waiting_for_path = 3
    state_stalling = 4

class OrderState(Enum):
    state_waiting_for_target = 1
    state_moving_to_target = 2
    state_waiting_for_order = 3

class UnitPriority(Enum):
    state_lowest = 1
    state_low = 2
    state_medium = 3
    state_high = 4
    state_highest = 5
