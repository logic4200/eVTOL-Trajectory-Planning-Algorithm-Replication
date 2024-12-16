import math
import random
import time

import matplotlib.pyplot as plt
import numpy as np

import a_star
import theta_star

random.seed(42)
# 定义栅格的尺寸
x_size = 100
y_size = 100
z_size = 150

# 定义起点和终点
start = (20, 20, 20)
end = (80, 80, 100)

# 创建3D栅格
grid_3d = np.zeros((x_size, y_size, z_size), dtype=bool)
grid_3d_safe = np.zeros((x_size, y_size, z_size), dtype=bool)

# 定义建筑物的数量
num_buildings = 50

# 安全裕度
safety_margin = 5


# 检查建筑物是否覆盖起始点或终点
def is_valid_building(x_start, y_start, length, width, height, safety_margin):
    for i in range(max(0, x_start - safety_margin), min(x_size, x_start + length + safety_margin)):
        for j in range(max(0, y_start - safety_margin), min(y_size, y_start + width + safety_margin)):
            for k in range(max(0, 0 - safety_margin), min(z_size, height + safety_margin)):
                if (i, j, k) == start or (i, j, k) == end:
                    return False
    return True


# 随机生成建筑物
for _ in range(num_buildings):
    while True:
        # 随机生成建筑物的长度、宽度和高度
        length = random.randint(8, 12)
        width = random.randint(6, 9)
        height = random.randint(30, 90)

        # 随机生成建筑物的起始位置
        x_start = random.randint(0, x_size - length)
        y_start = random.randint(0, y_size - width)

        # 检查建筑物是否覆盖起始点或终点
        if is_valid_building(x_start, y_start, length, width, height, safety_margin):
            break

    # 设置建筑物在栅格中的位置
    grid_3d[x_start:x_start + length, y_start:y_start + width, 0:height] = True
    grid_3d_safe[x_start:x_start + length, y_start:y_start + width, 0:height] = True

    # 增加安全裕度
    for i in range(max(0, x_start - safety_margin), min(x_size, x_start + length + safety_margin)):
        for j in range(max(0, y_start - safety_margin), min(y_size, y_start + width + safety_margin)):
            for k in range(max(0, 0 - safety_margin), min(z_size, height + safety_margin)):
                grid_3d_safe[i, j, k] = True


def calculate_path_length(path):
    if len(path) < 2:
        return 0

    total_length = 0
    for i in range(1, len(path)):
        x1, y1, z1 = path[i - 1]
        x2, y2, z2 = path[i]
        distance = math.sqrt(((x2 - x1) * 5) ** 2 + ((y2 - y1) * 5) ** 2 + (z2 - z1) ** 2)
        total_length += distance

    return total_length


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


# 执行算法
start_time = time.time()
path1 = a_star.a_star_search(grid_3d_safe, start, end, x_size, y_size, z_size)
path1_end_time = time.time()
dot_list = path1
dot = end
path2 = [dot]
while dot in dot_list and dot != start:
    for i in dot_list:
        if line_of_sight(dot, i, grid_3d_safe):
            dot = i
            path2.append(dot)
            break
path2 = path2[::-1]
path2_end_time = time.time()
path3 = theta_star.theta_star_search(grid_3d_safe, start, end, x_size, y_size, z_size)
path3_end_time = time.time()

length1 = calculate_path_length(path1)
length2 = calculate_path_length(path2)
length3 = calculate_path_length(path3)

print(f"Real length of path1: {length1}, cost time: {path1_end_time - start_time} s")
print(f"Real length of path2: {length2}, cost time: {path2_end_time - start_time} s")
print(f"Real length of path3: {length3}, cost time: {path3_end_time - path2_end_time} s")

# 绘制3D图形
fig = plt.figure(figsize=(12, 7))

# 第一个子图：3D视图
ax1 = fig.add_subplot(121, projection='3d')
ax1.voxels(grid_3d, facecolors='blue', alpha=0.5)
if path1:
    path_x = [p[0] for p in path1]
    path_y = [p[1] for p in path1]
    path_z = [p[2] for p in path1]
    ax1.plot(path_x, path_y, path_z, color='r', linestyle='-', linewidth=2)
if path2:
    path2_x = [p[0] for p in path2]
    path2_y = [p[1] for p in path2]
    path2_z = [p[2] for p in path2]
    ax1.plot(path2_x, path2_y, path2_z, color='yellow', linestyle='-', linewidth=2)
if path3:
    path3_x = [p[0] for p in path3]
    path3_y = [p[1] for p in path3]
    path3_z = [p[2] for p in path3]
    ax1.plot(path3_x, path3_y, path3_z, color='green', linestyle='-', linewidth=2)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('3D View')
ax1.set_xlim(0, x_size)
ax1.set_ylim(0, y_size)
ax1.set_zlim(0, z_size)

# 第二个子图：俯视图
ax2 = fig.add_subplot(122, projection='3d')
ax2.voxels(grid_3d, facecolors='blue', alpha=0.5)
if path1:
    path_x = [p[0] for p in path1]
    path_y = [p[1] for p in path1]
    path_z = [p[2] for p in path1]
    ax2.plot(path_x, path_y, path_z, color='r', linestyle='-', linewidth=2)
if path2:
    path2_x = [p[0] for p in path2]
    path2_y = [p[1] for p in path2]
    path2_z = [p[2] for p in path2]
    ax2.plot(path2_x, path2_y, path2_z, color='yellow', linestyle='-', linewidth=2)
if path3:
    path3_x = [p[0] for p in path3]
    path3_y = [p[1] for p in path3]
    path3_z = [p[2] for p in path3]
    ax2.plot(path3_x, path3_y, path3_z, color='green', linestyle='-', linewidth=2)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Top View')
ax2.set_xlim(0, x_size)
ax2.set_ylim(0, y_size)
ax2.set_zlim(0, z_size)
ax2.view_init(elev=90, azim=-90)  # 调整视角为俯视图

# 显示图形
plt.tight_layout()
plt.show()
