import random
import math
import pygame
from enum import Enum
from entity.mob.mob import Mob
from states.states import MovementState
from level.pathfinding.findpath import find_path
from graphics.sprite.spritesheet import SpriteSheet
from graphics.sprite.animatedsprite import AnimatedSprite

class Unit(Mob):

    def __init__(self, level, x, y):
        super().__init__(level, x, y, 2, 100)
        self.sprite = AnimatedSprite(level.sprite_group, "../res/soldier_spritesheet.png", x, y, 5)
        self.hor_spritesheet = self.sprite.spritesheet
        self.ver_spritesheet = SpriteSheet("../res/soldier_spritesheet.png")
        self.next = 0
        self.start = (0, 0)
        self.goal = None
        self.path = None
        self.movement_state = MovementState.state_reached_goal

    def tick(self):
        xa = 0
        ya = 0
        self.last_start = self.start
        self.start = (int(self.x + 16) >> 5, int(self.y + 16) >> 5)
        if self.last_start != self.start:
            self.level.set_occupied(self.last_start[0], self.last_start[1], False)
            self.level.set_occupied(self.start[0], self.start[1], True)
        if self.movement_state == MovementState.state_waiting_for_path:
            if self.goal and not self.level.get_tile(self.start[0], self.start[1]).solid and not self.level.get_tile(self.goal[0], self.goal[1]).solid:                
                self.path = find_path(self.level, self.start, self.goal)
                #if not self.path:
                #print("(%d, %d) and (%d, %d)" % (self.start[0], self.start[1], self.goal[0], self.goal[1]))
                self.movement_state = MovementState.state_moving


        if self.movement_state == MovementState.state_moving:
            if not self.path or (self.x, self.y) == (self.goal[0] << 5, self.goal[1] << 5):
                self.movement_state = MovementState.state_reached_goal
            else:
                if len(self.path) > 0:
                    pos = self.path[-1]
                    pos = (pos[0] << 5, pos[1] << 5)
                    if (self.x, self.y) == (pos[0], pos[1]): #TODO change logic to do proper moves!!                        
                        self.path.pop()
                        if len(self.path) > 0:
                            pos = self.path[-1]
                    '''
                    if self.x < pos[0]:
                        xa += min(pos[0] - self.x, self.speed)
                    if self.x > pos[0]:
                        xa -= min(self.x - pos[0], self.speed)
                    if self.y < pos[1]:
                        ya += min(pos[1] - self.y, self.speed)
                    if self.y > pos[1]:
                        ya -= min(self.y - pos[1], self.speed)
                    '''
                    if self.level.updates % 15 == 0:
                        self.x = pos[0]
                        self.y = pos[1]
                else:
                    self.movement_state = MovementState.state_reached_goal

        if xa or ya:
            self.movement_state = MovementState.state_moving
            if not self.move(xa, ya):
                self.movement_state = MovementState.state_waiting_for_path

        if self.moving_dir < 2:
            self.sprite.set_spritesheet(self.hor_spritesheet)
        else:
            self.sprite.set_spritesheet(self.ver_spritesheet)
        if self.moving_dir == 1 or self.moving_dir == 3:
            self.sprite.set_flipped(True)
        self.sprite.set_position(self.x, self.y)
        if self.movement_state == MovementState.state_moving:
            self.sprite.tick()
        else:
            self.sprite.current_frame = 0
            self.sprite.load(0)

    def goto(self, pos):
        self.goal = pos
        self.movement_state = MovementState.state_waiting_for_path

    def distance(self, start, goal):
        return math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

    def has_collided(self, xa, ya):
        rect = pygame.Rect(self.x + xa, self.y + ya, 32, 32)
        for sprite in self.level.sprite_group:
            if sprite is not self.sprite:
                if rect.colliderect(sprite.posrect):
                    return True
        return False

    def render(self, x_offset, y_offset):
        self.sprite.render(x_offset, y_offset)