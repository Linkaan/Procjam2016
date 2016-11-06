import pygame

class Texture(object):

    def __init__(self, path):
        try:
            self.img = pygame.image.load(path).convert()
        except pygame.error, message:
            print 'Unable to load texture from file:', path
            raise SystemExit, message

Textures = dict(
    VOID=Texture("../res/void.png"),
    ROAD=Texture("../res/road.png"),
    WALL=Texture("../res/wall.png")
)
