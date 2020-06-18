from matplotlib import colors
from matplotlib.animation import ArtistAnimation
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib
matplotlib.use("Agg")


class Agent():
    def __init__(self, start, target, route):
        self.start = start
        self.target = None
        self.route = None


def split_by_char(line):
    return [char for char in line]


def process_layout(layout):
    lines = []
    for line in layout:
        line = line.replace('\n', '')
        lines.append(line)

    maze = [split_by_char(line) for line in lines]

    agents = []
    targets = []

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'A':
                agents.append((j, i))
                maze[i][j] = ' '
            elif maze[i][j] == 'T':
                targets.append((j, i))
                maze[i][j] = ' '

    # print(maze)
    # print(agents)
    # print(targets)

    return maze, agents, targets


def reconstruct_path(maze, prev, start, end, waits):

    # print('reconstruct path called')
    # print(prev)

    node = end

    path = []
    print('what is given to reconstruct:')
    print(prev)
    # print('nodes:')
    while node != start:
        # print(node)
        path.append(node)
        node = prev[node]

    path.append(start)

    path.reverse()
    print('reconstruct_path')
    print(path)

    for w in range(len(waits)):
        if waits[w] in path:
            i = path.index(waits[w])
            print(i)
            if i > 0:
                path.insert(i - 1, path[i-1])

    # print(path)
    # print()
    # print()
    # print()
    path_dict = {}
    for i in range(len(path)):
        path_dict[i] = path[i]

    # print(path_dict)
    # print()
    # print()
    # print()
    # print()
    # print()
    # print()
    # print(path_dict)

    # for node in path:
    #     if node != start and node != end:
    #         maze.layout[node[1]][node[0]] = 'P'

    return path_dict


def get_distance(open_node, neighbour):
    dy = neighbour[0] - open_node[0]
    dx = neighbour[1] - open_node[1]
    return math.sqrt(dx**2 + dy**2)


def get_manhattan_distance(open_node, neighbour):
    dy = neighbour[0] - open_node[0]
    dx = neighbour[1] - open_node[1]
    return abs(dy)+abs(dx)


def transform_array_to_int(array, steps):
    int_array = np.zeros((len(array), len(array[0])))

    color_index = 0
    for step in steps:
        int_array[step[1]][step[0]] = 4

    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == 'X':
                int_array[i][j] = 1
            elif array[i][j] == 'S':
                int_array[i][j] = 2
            elif array[i][j] == 'E':
                int_array[i][j] = 3

    return int_array.astype(np.int)


def plot_paths(layout, paths):
    images = []

    cmap = colors.ListedColormap(['white', 'black', 'red', 'green', 'blue'])

    lengths = [len(path) for path in paths]
    lengths.sort()
    longest_path = lengths[-1]

    # print(longest_path)
    fig = plt.figure()
    for i in range(longest_path):

        # plt.axis([0, 8, 0, 20])

        steps = []
        for path in paths:
            if path.get(i) != None:
                steps.append(path.get(i))

        layout_arr = transform_array_to_int(layout, steps)

        img = plt.pcolor(layout_arr[::-1], cmap=cmap,
                         edgecolors='k', linewidths=1)
        images.append([img])

    # plt.xlabel('pořadí')
    # plt.ylabel('přirozená čísla')
    # print(images)
    animation = ArtistAnimation(fig, images, interval=400)
    print('Kroků animace:', len(images))
    animation.save('anim.mp4', dpi=800)


def import_current_constraints(constraints, timestep):
    # print(constraints)
    # print(timestep)

    current_constraints = []
    for c in constraints:
        # print(c[0], timestep)
        if c[0] == timestep + 1:
            current_constraints.append(c[1])
    # print('current constraints ', current_constraints)
    return current_constraints


def is_occupied(neighbour, current_constraint):
    occupied = False

    # print(neighbour, 'neighbour')
    # print(current_constraint, 'cc')

    for cc in current_constraint:
        if cc == neighbour:
            occupied = True
            print('deadlock', cc, neighbour)

    return occupied
