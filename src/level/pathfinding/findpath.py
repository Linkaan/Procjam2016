from level.pathfinding.node import Node

def find_path(level, start, goal):
    open_list = []
    closed_list = []
    current = Node(start, None, 0, distance(start, goal))
    open_list.append(current)
    while len(open_list) > 0:
        open_list.sort(key=lambda x: x.f_cost, reverse=True)
        current = open_list.pop(0)
        if current.pos == goal:
            path = []
            while current.path:
                path.append(current)
                current = current.parent
            del open_list
            del closed_list
            return path
        closed_list.append(current)
        for i in range(8):
            x = current.pos[0]
            y = current.pos[1]
            xi = (i % 3) - 1
            xy = (i / 3)  -1
            a = (x + xi, y + yi)
            at = level.get_tile(a[0], a[1])
            if at.solid: continue
            g_cost = current.g_cost + (distance(current.pos, a) > 1 ? 0.95 : 1) + 1 #at.g_cost
            h_cost = distance(a, goal)
            node = Node(a, current, g_cost, h_cost)
            if is_pos_in_nodes(a, closed_list) and g_cost >= node.g_cost: continue
            if not is_pos_in_nodes(a, open_list) or g_cost < node.g_cost: open_list.append(node)
    del closed_list
    return None

def distance(start, goal):
    return math.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

def is_pos_in_nodes(pos, nodes):
    for node in nodes:
        if node.pos == pos: return True
    return False
