from level.tiles.tile import Tile

class BasicTile(Tile):

    def __init__(self, tileid, tex):
        super().__init__(tileid, False)
        self.tex = tex

    def render(self, surface, x, y):
        surface.blit(self.tex.img, (x, y, 32, 32))

    def tick(self):
        pass

class BasicSolidTile(BasicTile):

    def __init__(self, tileid, tex):
        super().__init__(tileid, tex)
        self.solid = True
