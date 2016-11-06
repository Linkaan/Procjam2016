from entity.pickups.pickup import Pickup
from graphics.sprite.basicsprite import BasicSprite

class BazookaPickup(Pickup):

    def __init__(self, level, x, y):
        super().__init__(level, x, y, BasicSprite("../res/bazooka.png", x, y))
