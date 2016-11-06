from graphics.textures import Textures
from level.tiles.basictile import BasicTile, BasicSolidTile

VOID = BasicSolidTile(0, Textures["VOID"])
ROAD = BasicTile(1, Textures["ROAD"])
WALL = BasicSolidTile(2, Textures["WALL"])
