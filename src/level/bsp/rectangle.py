class Rect(object):

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h
        self.w = w
        self.h = h
        self.center = (int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2))

    def contains(self, x, y):
        if (self.w | self.h) < 0:
            return False
        if x < self.x or y < self.y:
            return False
        return ((self.x2 < self.x or self.x2 > x) and
                (self.y2 < self.y or self.y2 > y))

    def intersects(self, rect):
        return (self.x1 <= rect.x2 and
                self.x2 >= rect.x1 and
                self.y1 <= rect.y2 and
                self.y2 >= rect.y1)
