class Node(object):

    def __init__(self, pos, parent, g_cost, h_cost):
        self.pos = pos
        self.parent = parent
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
