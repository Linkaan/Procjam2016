import pygame

class SpriteSheet(object):

    def __init__(self, path, frames=None):
        try:
            self.sheet = pygame.image.load(path).convert_alpha()
        except pygame.error as message:
            print("Unable to load spritesheet image: " + path)
            raise SystemExit(message)
        rect = self.sheet.get_rect()
        self.width = rect.width
        self.height = rect.height
        self.sprites = []
        tx = self.width >> 5
        ty = self.height >> 5
        frames = frames or tx * ty
        for i in range(0, frames):
            x = i % tx
            y = int(i / tx)
            self.sprites.append(self.image_at((x<<5, y<<5, 32, 32)))

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
        image.blit(self.sheet, (0, 0), rect)
        return image
