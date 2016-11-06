from graphics.texture import Texture

Textures = dict(
    VOID=Texture("../res/void.png"),
    ROAD=Texture("../res/road.png"),
    WALL=Texture("../res/wall.png")
)

def load_textures():
    for t in Textures:
        Textures[t].load()
