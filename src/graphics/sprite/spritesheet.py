import pygame

class SpriteSheet(object):

    def __init__(self, path):
        try:
            self.sheet = pygame.image.load(path).convert_alpha()
        except pygame.error as message:
            print("Unable to load spritesheet image: " + path)
            raise SystemExit(message)
        rect = self.sheet.get_rect()
        self.width = rect.width
        self.height = rect.height
        self.sprites = []
        for y in range(0, self.height, 32):
            for x in range(0, self.width, 32):
                self.sprites.append(self.image_at((x, y, 32, 32)))

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
        image.blit(self.sheet, (0, 0), rect)
        return image
