import pygame

class Texture(object):

    def __init__(self, path):
        self.img = pygame.image.load(path)

Textures = dict(
    VOID=Texture("../res/void.png"),
    ROAD=Texture("../res/road.png"),
    WALL=Texture("../res/wall.png")
)
