import pygame
from graphics.sprite.sprite import Sprite

class AnimatedSprite(Sprite):

    def __init__(self, path, delay):
        super().__init__(path)
        self.src_sprites = self.sprites[:]
        self.delay = delay
        self.tick = 0
        self.current_frame = 0

    def set_flipped(self, is_flipped):
        if is_flipped:
            for s in enumerate(self.src_sprites):
                self.sprites[s[0]] = pygame.transform.rotate(s[1], 180)
        else:
            self.sprites = self.src_sprites[:]

    def tick(self):
        self.tick += 1
        if self.tick == self.delay:
            self.current_frame += 1
            self.tick = 0
        if self.current_frame == len(self.sprites):
            self.current_frame = 0

    def render(self, screen, x_offset, y_offset):
        x = self.x - x_offset
        y = self.y - y_offset
        if 0 > x or x >= SCREEN_SIZE[0] or 0 > y or y >= SCREEN_SIZE[1]:
            continue
        self.rect = self.sprites[current_frame].get_rect()
        self.rect.center = (x, y)
        self.sprite_group.draw(screen)
