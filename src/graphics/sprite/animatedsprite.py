import pygame
from GameConfig import *
from graphics.sprite.sprite import Sprite

class AnimatedSprite(Sprite):

    def __init__(self, group, path, x, y, delay):
        super().__init__(group, path, x, y)
        self.src_sprites = self.sprites[:]
        self.delay = delay
        self.updates = 0
        self.current_frame = 0
        self.load(self.current_frame)
        self.flipped = False

    def set_flipped(self, is_flipped):
        if self.flipped == is_flipped:
            return
        self.flipped = is_flipped
        if is_flipped:
            for s in enumerate(self.src_sprites):
                self.sprites[s[0]] = pygame.transform.flip(s[1], True, False)
        else:
            self.sprites = self.src_sprites[:]

    def set_spritesheet(self, spritesheet):
        if self.spritesheet is spritesheet:
            return
        self.spritesheet = spritesheet
        self.sprites = spritesheet.sprites
        self.src_sprites = self.sprites[:]
        self.current_frame = 0
        self.load(self.current_frame)
        self.flipped = False

    def tick(self):
        self.updates += 1
        if self.updates == self.delay:
            self.current_frame += 1
            self.updates = 0
        if self.current_frame == len(self.sprites):
            self.current_frame = 0
        self.load(self.current_frame)

    def render(self, x_offset, y_offset):
        x = self.x - x_offset + 16
        y = self.y - y_offset + 16
        if 0 > x or x >= SCREEN_SIZE[0] or 0 > y or y >= SCREEN_SIZE[1]:
            return
        self.rect = self.sprites[self.current_frame].get_rect()
        self.rect.center = (x, y)
        self.render_flag = True
