import heapq

cimport cython
@cython.boundscheck(False)
def cfind_path(level, start, goal):
    open_set = set()
    open_heap = []
    closed_set = set()
    came_from = {}

    cdef int tentative_g_score, node_g_score

    g_score = {}
    f_score = {}

    g_score[start] = 0
    f_score[start] = manhattandistance(start[0], start[1], goal[0], goal[1])
    open_set.add(start)
    open_heap.append((0, start))
    while open_set:
        current = heapq.heappop(open_heap)[1]
        if current == goal:
            return reconstruct_path(came_from, current)
        open_set.remove(current)
        closed_set.add(current)
        for node in level.graph[current]:
            if node not in closed_set: # and not level.is_occupied(node[0], node[1])
                tentative_g_score = g_score.get(current, 256) + 1
                node_g_score = g_score.get(node, 256)
                if node not in open_set:
                    open_set.add(node)
                    heapq.heappush(open_heap, (f_score.get(node, 256), node))
                elif tentative_g_score >= node_g_score:
                    continue

                came_from[node] = current
                g_score[node] = tentative_g_score
                f_score[node] = node_g_score + manhattandistance(node[0], node[1], goal[0], goal[1])
    return None

@cython.boundscheck(False)
cdef reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path

@cython.boundscheck(False)
cdef int manhattandistance(int x1, int y1, int x2, int y2):
    return abs(x2 - x1) + abs(y2 - y1)
