class Node(object):

    def __init__(self, pos):
        self.pos = pos
        self.parent = None
        self.h_cost = 0
        self.visited = False

    def update_node(self, parent, h_cost):
        self.parent = parent
        self.h_cost = h_cost

    def set_visited(self, visited):
        self.visited = visited
        if not visited:
            self.parent = None
            self.h_cost = 0

    def __lt__(self, other):
        return self.h_cost < other.h_cost
