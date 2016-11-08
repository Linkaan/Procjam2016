from enum import Enum

class FormationState(Enum):
    state_broken = 1
    state_forming = 2
    state_formed = 3

class MovementState(Enum):
    state_moving = 1
    state_reached_goal = 2
    state_waiting_for_path = 3