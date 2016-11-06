import random
from GameConfig import *
from level.bsp.rectangle import Rect

class Leaf(object):

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.room = None
        self.halls = None
        self.left_child = None
        self.right_child = None

    def get_room(self):
        if self.room:
            return self.room
        else:
            l_room = None
            r_room = None
            if self.left_child:
                l_room = self.left_child.get_room()
            if self.right_child:
                r_room = self.right_child.get_room()
            if not l_room and not r_room:
                return None
            elif r_room is None:
                return l_room
            elif l_room is None:
                return r_room
            else:
                return random.choice([l_room, r_room])

    def create_hall(self, l, r):
        self.halls = []

        point1 = (random.randint(l.x1 + 1, l.x2 - 2), random.randint(l.y1 + 1, l.y2 - 2))
        point2 = (random.randint(r.x1 + 1, r.x2 - 2), random.randint(r.y1 + 1, r.y2 - 2))

        w = point2[0] - point1[0]
        h = point2[1] - point1[1]

        if w < 0:
            if h < 0:
                self.halls.append(random.choice([Rect(point2[0], point1[1], abs(w), 1), Rect(point2[0], point2[1], abs(w), 1)]))
                self.halls.append(random.choice([Rect(point2[0], point2[1], 1, abs(h)), Rect(point1[0], point2[1], 1, abs(h))]))
            elif h > 0:
                self.halls.append(random.choice([Rect(point2[0], point1[1], abs(w), 1), Rect(point2[0], point2[1], abs(w), 1)]))
                self.halls.append(random.choice([Rect(point2[0], point1[1], 1, abs(h)), Rect(point1[0], point1[1], 1, abs(h))]))
            else:
                self.halls.append(Rect(point2[0], point2[1], abs(w), 1))
        elif w > 0:
            if h < 0:
                self.halls.append(random.choice([Rect(point1[0], point2[1], abs(w), 1), Rect(point1[0], point1[1], abs(w), 1)]))
                self.halls.append(random.choice([Rect(point1[0], point2[1], 1, abs(h)), Rect(point2[0], point2[1], 1, abs(h))]))
            elif h > 0:
                self.halls.append(random.choice([Rect(point1[0], point1[1], abs(w), 1), Rect(point1[0], point2[1], abs(w), 1)]))
                self.halls.append(random.choice([Rect(point2[0], point1[1], 1, abs(h)), Rect(point1[0], point1[1], 1, abs(h))]))
            else:
                self.halls.append(Rect(point1[0], point1[1], abs(w), 1))
        else:
            assert h != 0
            if h < 0:
                self.halls.append(Rect(point2[0], point2[1], 1, abs(h)))
            elif h > 0:
                self.halls.append(Rect(point1[0], point1[1], 1, abs(h)))

    def create_rooms(self):
        if self.left_child or self.right_child:
            if self.left_child:
                self.left_child.create_rooms()
            if self.right_child:
                self.right_child.create_rooms()
            if self.left_child and self.right_child:
                self.create_hall(self.left_child.get_room(), self.right_child.get_room())
        else:
            room_size = (random.randint(MIN_ROOM_WIDTH, self.width - 2), random.randint(MIN_ROOM_HEIGHT, self.height - 2))
            room_pos = (random.randint(1, self.width - room_size[0] - 1), random.randint(1, self.height - room_size[1] - 1))
            self.room = Rect(self.x + room_pos[0], self.y + room_pos[1], room_size[0], room_size[1])

    def split(self):
        if self.left_child or self.right_child:
            return False

        split_h = random.random() < 0.5
        if self.width > self.height and self.height / self.width >= 0.05:
            split_h = False
        elif self.height > self.width and self.width / self.height >= 0.05:
            split_h = True

        _max = (self.height if split_h else self.width) - MIN_LEAF_SIZE
        if _max <= MIN_LEAF_SIZE:
            return False

        split = random.randint(MIN_LEAF_SIZE, _max)
        if split_h:
            self.left_child = Leaf(self.x, self.y, self.width, split)
            self.right_child = Leaf(self.x, self.y + split, self.width, self.height - split)
        else:
            self.left_child = Leaf(self.x, self.y, split, self.height)
            self.right_child = Leaf(self.x + split, self.y, self.width - split, self.height)
        return True
