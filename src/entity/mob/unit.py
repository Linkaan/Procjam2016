import random
import pygame
from entity.mob.mob import Mob
from level.pathfinding.findpath import find_path
from graphics.sprite.animatedsprite import AnimatedSprite

class Unit(Mob):

    def __init__(self, level, x, y):
        super().__init__(level, x, y, 2, 100)
        self.vsprite = AnimatedSprite("../res/soldier_spritesheet.png", x, y, 5)
        self.hsprite = AnimatedSprite("../res/soldier_spritesheet.png", x, y, 5)
        self.sprite = self.hsprite
        self.updates = 0
        self.next = 0
        self.goal = (x, y)
        self.last_goal = self.goal
        self.path = None
        self.x_offset = 0
        self.y_offset = 0

    def tick(self):
        xa = 0
        ya = 0
        mouse_pos = pygame.mouse.get_pos()
        self.goal = ((mouse_pos[0] + self.x_offset) >> 5, (mouse_pos[1] + self.y_offset) >> 5)
        start = (int(self.x + 16) >> 5, int(self.y + 16) >> 5)
        if self.goal != self.last_goal:
            if not self.level.get_tile(start[0], start[1]).solid and not self.level.get_tile(self.goal[0], self.goal[1]).solid:
                print("(%d, %d) and (%d, %d)" % (start[0], start[1], self.goal[0], self.goal[1]))
                self.path = find_path(self.level, start, self.goal)
                self.last_goal = self.goal

        if start != self.last_goal:
            if self.path:
                if len(self.path) > 0:
                    pos = self.path[-1]
                    if start == pos:
                        self.path.pop()
                        pos = self.path[-1]
                    pos = (pos[0] << 5, pos[1] << 5)
                    if self.x < pos[0]:
                        xa += self.speed
                    if self.x > pos[0]:
                        xa -= self.speed
                    if self.y < pos[1]:
                        ya += self.speed
                    if self.y > pos[1]:
                        ya -= self.speed

        if xa or ya:
            self.moving = True
            self.move(xa, ya)
        else:
            self.moving = False

        if self.moving_dir < 2:
            self.sprite = self.hsprite
        else:
            self.sprite = self.vsprite
        if self.moving_dir == 1 or self.moving_dir == 3:
            self.sprite.set_flipped(True)
        self.sprite.set_position(self.x, self.y)
        if self.moving:
            self.sprite.tick()
        else:
            self.sprite.current_frame = 0
            self.sprite.load(0)
        self.updates += 1

    def render(self, surface, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.sprite.render(surface, x_offset, y_offset)
