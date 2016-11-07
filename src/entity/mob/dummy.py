import random
from entity.mob.mob import Mob
from graphics.sprite.animatedsprite import AnimatedSprite

class Dummy(Mob):

    def __init__(self, level, x, y):
        super().__init__(level, x, y, 1, 100)
        self.vsprite = AnimatedSprite("../res/soldier_spritesheet.png", x, y, 5)
        self.hsprite = AnimatedSprite("../res/soldier_spritesheet.png", x, y, 5)
        self.sprite = self.hsprite
        self.updates = 0
        self.next = 0
        self.goal = (x, y)

    def tick(self):
        xa = 0
        ya = 0
        if self.updates - self.next >= 0: # and (self.x, self.y) == self.goal
             self.next += random.randint(60, 450)
             self.goal = (-1, -1)
             while self.level.get_tile(self.goal[0]>>5, self.goal[1]>>5).solid:
                 self.goal = (self.x + (random.randint(-5, 5)<<5), self.y + (random.randint(-5, 5)<<5))

        if self.x < self.goal[0]:
            xa += self.speed
        if self.x > self.goal[0]:
            xa -= self.speed
        if self.y < self.goal[1]:
            ya += self.speed
        if self.y > self.goal[1]:
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
        self.sprite.render(surface, x_offset, y_offset)
