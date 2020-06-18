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

    return maze, agents, targets


def reconstruct_path(maze, prev, start, end, waits):
    node = end

    path = []
    while node != start:
        path.append(node)
        node = prev[node]

    path.append(start)

    path.reverse()

    for w in range(len(waits)):
        if waits[w] in path:
            i = path.index(waits[w])
            if i > 0:
                path.insert(i - 1, path[i-1])

    path_dict = {}
    for i in range(len(path)):
        path_dict[i] = path[i]

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
    
    for step in steps:
        # if step != steps[0] or step != steps[-1]:
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

    fig = plt.figure()

    for i in range(longest_path):

        steps = []
        for path in paths:
            if path.get(i) != None:
                steps.append(path.get(i))

        # print(steps)
        layout_arr = transform_array_to_int(layout, steps)
        
        img = plt.pcolor(layout_arr[::-1], cmap=cmap,
                         edgecolors='k', linewidths=1)
        images.append([img])
        if i==0:
            plt.savefig('pics/start.png')

    images.insert(0,images[1])
    images.append(images[-1])


    animation = ArtistAnimation(fig, images, interval=250)
    print('Animation steps:', len(images))
    animation.save('video/anim.mp4', dpi=800)


def import_current_constraints(constraints, timestep):
    current_constraints = []
    for c in constraints:
        if c[0] == timestep + 1:
            current_constraints.append(c[1])
    return current_constraints


def is_occupied(neighbour, current_constraint):
    occupied = False

    for cc in current_constraint:
        if cc == neighbour:
            occupied = True
            print('Deadlock at position: ', cc, neighbour)

    return occupied
