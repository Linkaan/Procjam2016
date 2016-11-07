import abc
import pygame
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from graphics.sprite.spritesheet import SpriteSheet

class Sprite(pygame.sprite.Sprite):
    __metaclass__ = ABCMeta

    def __init__(self, group, path, x, y):
        super().__init__(group)
        self.x = x
        self.y = y
        self.render_flag = False
        self.spritesheet = SpriteSheet(path)
        self.sprites = self.spritesheet.sprites
        self.posrect = pygame.Rect(x, y, 32, 32)

    def load(self, sprite_num):
        self.image = self.sprites[sprite_num]

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.posrect.x = x
        self.posrect.y = y

    @abstractmethod
    def tick(self):
        pass

    @abstractproperty
    def render(self, x_offset, y_offset):
        pass
