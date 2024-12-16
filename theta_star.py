import heapq
import math


def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)

def line_of_sight(s1, s2, grid):
    dx = s2[0] - s1[0]
    dy = s2[1] - s1[1]
    dz = s2[2] - s1[2]
    steps = max(abs(dx), abs(dy), abs(dz))
    x, y, z = s1[0], s1[1], s1[2]
    delta_x = dx / steps
    delta_y = dy / steps
    delta_z = dz / steps
    for i in range(steps):
        x += delta_x
        y += delta_y
        z += delta_z
        ix, iy, iz = int(x), int(y), int(z)
        if (0 <= ix < len(grid) and
                0 <= iy < len(grid[0]) and
                0 <= iz < len(grid[0][0])):
            if grid[ix][iy][iz]:
                return False
    return True

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)

def theta_star_search(grid, start, end, x_size, y_size, z_size):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    directions = [(-1, -1, -1), (-1, -1, 0), (-1, -1, 1), (-1, 0, -1), (-1, 0, 0), (-1, 0, 1), (-1, 1, -1), (-1, 1, 0),
                  (-1, 1, 1), (0, -1, -1), (0, -1, 0), (0, -1, 1), (0, 0, -1), (0, 0, 1), (0, 1, -1), (0, 1, 0),
                  (0, 1, 1), (1, -1, -1), (1, -1, 0), (1, -1, 1), (1, 0, -1), (1, 0, 0), (1, 0, 1), (1, 1, -1),
                  (1, 1, 0), (1, 1, 1)]

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy, dz in directions:
            neighbor = (current[0] + dx, current[1] + dy, current[2] + dz)
            if 0 <= neighbor[0] < x_size and 0 <= neighbor[1] < y_size and 0 <= neighbor[2] < z_size:
                if grid[neighbor[0], neighbor[1], neighbor[2]]:
                    continue
                else:
                    if neighbor not in g_score:
                        if neighbor not in open_set:
                            g_score[neighbor] = float('inf')
                        parent = came_from.get(current)
                        if parent is None:
                            parent = start
                        if line_of_sight(parent, neighbor, grid):
                            tentative_g_score = g_score[parent] + distance(neighbor, parent)
                            if tentative_g_score < g_score[neighbor]:
                                came_from[neighbor] = parent
                                g_score[neighbor] = tentative_g_score
                                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        else:
                            # 计算移动代价，对角线移动代价更高
                            if abs(dx) + abs(dy) + abs(dz) == 1:
                                move_cost = 1
                            elif abs(dx) + abs(dy) + abs(dz) == 2:
                                move_cost = 1.414
                            elif abs(dx) + abs(dy) + abs(dz) == 3:
                                move_cost = 1.732
                            tentative_g_score = g_score[current] + move_cost
                            if tentative_g_score < g_score[neighbor]:
                                came_from[neighbor] = current
                                g_score[neighbor] = tentative_g_score
                                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None