from termcolor import colored, cprint
import os
import time
import utils
import numpy as np

from a_star import run_a_star
from alocate_targets import alocate


class Maze():

    def __init__(self, layout, original_layout, agents, targets):
        self.layout = layout
        self.original_layout = original_layout
        self.agents = agents
        self.targets = targets

    def print_maze(self, clear=False):
        if clear:
            os.system('cls' if os.name == 'nt' else 'clear')

        for i in range(len(self.layout)):
            for j in range(len(self.layout[0])):
                if self.layout[i][j] == 'X':  # wall
                    cprint('\u2588\u2588', 'grey', end='')
                elif self.layout[i][j] == ' ':    # fresh node
                    cprint('\u2588\u2588', 'white', end='')
                elif self.layout[i][j] == 'S':    # start
                    cprint('\u2588\u2588', 'green', end='')
                elif self.layout[i][j] == 'E':    # end
                    cprint('\u2588\u2588', 'red', end='')
                elif self.layout[i][j] == 'O':    # opened
                    cprint('\u2588\u2588', 'yellow', end='')
                elif self.layout[i][j] == 'P':    # path
                    cprint('\u2588\u2588', 'blue', end='')
            print()

    def print_path(self, path):
        for value in path.values():
            self.layout[value[1]][value[0]] = 'P'
        self.print_maze()
        for value in path.values():
            self.layout[value[1]][value[0]] = ' '

    # def setup_start_end(self):
    #     self.layout[self.start[1]][self.start[0]] = 'S'
    #     self.layout[self.end[1]][self.end[0]] = 'E'

    def get_neighbours(self, node):
        y, x = node
        neighbours = [(y + 1, x), (y, x + 1), (y-1, x), (y, x - 1), (y, x)]
        return neighbours

    def report(self, name):
        self.print_maze()

        opened_counter = 0
        path_counter = 0

        for i in range(len(self.layout)):
            for j in range(len(self.layout[0])):
                if self.layout[i][j] == 'O':    # opened
                    opened_counter += 1
                elif self.layout[i][j] == 'P':    # path
                    path_counter += 1
        opened_counter += path_counter

        print(30 * '-')
        print(name)
        print(30 * '-')
        cprint('\u2588\u2588', 'green', end='')
        print(' Start')
        cprint('\u2588\u2588', 'red', end='')
        print(' End')
        cprint('\u2588\u2588', 'yellow', end='')
        print(' Opened')
        cprint('\u2588\u2588', 'blue', end='')
        print(' Path')
        cprint('\u2588\u2588', 'grey', end='')
        print(' Wall')
        print(30 * '-')
        print('Nodes expanded:', opened_counter)
        print('Path length:', path_counter)


def find_conflicts():
    pass


def update_constraints(constraints, path):
    for key, value in path.items():
        constraints.append((key, value))
    return constraints


def run_solver(maze):
    paths = alocate(maze)

    sorted_paths = sorted(paths, key=lambda path: len(path), reverse=True)

    priority_path = sorted_paths.pop(0)
    constraints = []

    # constraints = [(3,(6,6)), (4,(6,6)), (5,(6,6)), (6,(6,6)), (7,(6,6)), (8,(6,6)), (9,(6,6)), (10,(6,6))]
    
    constraints = update_constraints(constraints, priority_path)
    
    # print(constraints)

    final_paths = []
    final_paths.append(priority_path)
    
    for path in sorted_paths:
        lock = False
        # print(path)
        for key, value in path.items():
            if (key, value) in constraints:
                lock = True
                break
        if lock:
            # print(path, ' path before')
            path = run_a_star(
                maze, maze.original_layout, path.get(
                    0), list(path.values())[-1],
                put_on_a_show=False, constraints=constraints)
            final_paths.append(path)
            print('returned')
            print(path)
            constraints = update_constraints(constraints, path)

    print(constraints)
    print('x'*200)
    # print('x'*200)
    # print('x'*200)
    
    utils.plot_paths(maze.original_layout, final_paths)

    # for pair in pairs:
    #     print(routes)
    #     route = run_a_star(maze, pair[0], pair[1], put_on_a_show=False, constraints=routes)
    #     routes.append(route)


def Main():
    layout = open('data/blocked_path.txt', 'r')

    maze, agents, targets = utils.process_layout(layout)
    maze = Maze(maze, maze, agents, targets)

    run_solver(maze)

    # run_a_star(maze, put_on_a_show=True)


Main()
