from graphics.sprite.sprite import Sprite

class BasicSprite(Sprite):

    def __init__(self, path):
        super().__init__(path)
        self.load(0)

    def render(self, screen, x_offset, y_offset):
        x = self.x - x_offset
        y = self.y - y_offset
        if 0 > x or x >= SCREEN_SIZE[0] or 0 > y or y >= SCREEN_SIZE[1]:
            continue
        self.rect = self.sprites[0].get_rect()
        self.rect.center = (x, y)
        self.sprite_group.draw(screen)
