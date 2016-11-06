import pygame

class Texture(object):

    def __init__(self, path):
        self.path = path

    def load(self):
        try:
            self.img = pygame.image.load(self.path).convert()
        except pygame.error as message:
            print("Unable to load texture from file: " + path)
            raise SystemExit(message)
