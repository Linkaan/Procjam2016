import abc
import pygame
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from graphics.sprite.spritesheet import SpriteSheet

class Sprite(pygame.sprite.Sprite):
    __metaclass__ = ABCMeta

    def __init__(self, path, x, y):
        self.x = x
        self.y = y
        self.sprite_group = pygame.sprite.RenderPlain(self)
        self.spritesheet = SpriteSheet(path)
        self.sprites = self.spritesheet.sprites

    def load(self, sprite_num):
        self.image = self.sprites[sprite_num]

    @abstractmethod
    def tick(self):
        pass

    @abstractproperty
    def render(self, screen, x_offset, y_offset):
        pass
