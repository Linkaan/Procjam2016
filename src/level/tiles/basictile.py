from level.tiles.tile import Tile

class BasicTile(Tile):

    def __init__(self, tileid, tex):
        super().__init__(tileid, False)
        self.tex = tex

    def render(self, level, surface, x, y):
        '''
        if 0 > x or x >= level.width << 5 or 0 > y or y >= level.height << 5:
            return
        '''
        surface.blit(self.tex.img, (x, y, 32, 32))

    def tick(self):
        pass

class BasicSolidTile(BasicTile):

    def __init__(self, tileid, tex):
        super().__init__(tileid, tex)
        self.solid = True
