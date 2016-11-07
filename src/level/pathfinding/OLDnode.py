class Node(object):

    def __init__(self, pos):
        self.pos = pos
        self.set_visited(False)

    def update_node(self, parent, g_cost, h_cost):
        self.parent = parent
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    def set_visited(self, visited):
        self.visited = visited
        if not visited:
            self.parent = None
            self.g_cost = 0
            self.h_cost = 0
            self.f_cost = 0

    def __lt__(self, other):
        return self.h_cost < other.h_cost
