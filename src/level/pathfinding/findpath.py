import math
import heapq

def find_path(level, start, goal):
    open_set = set()
    open_heap = []
    closed_set = set()

    open_set.add(start)
    open_heap.append((0, start))
    while open_set:
        current = heapq.heappop(open_heap)[1]
        if current == goal:
            path = []
            while current.parent:
                path.append(current)
                last = current
                current = current.parent
                last.set_visited(False)
            for node in closed_set:
                node.set_visited(False)
            return path
        current.set_visited(True)
        open_set.remove(current)
        closed_set.add(current)
        for node in level.graph[current.pos]:
            if node not in closed_set:
                h_cost = manhattandistance(node.pos, goal.pos)
                node.update_node(current, h_cost)
                if node not in open_set:
                    open_set.add(node)
                    heapq.heappush(open_heap, (node.h_cost, node))
    for node in closed_set:
        node.set_visited(False)
    return None

def manhattandistance(start, goal):
    return abs(goal[0]-start[0]) + abs(goal[1]-start[0]);
