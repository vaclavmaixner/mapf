import utils
import heapq


def run_a_star(maze, layout, start, end, put_on_a_show, constraints):
    queue = []
    closed = []
    prev = {}
    distance = {}

    heapq.heappush(queue, (0, start))
    distance[start] = 0

    timestep = 0

    # print(start, end, ' agent, target')
    # print(queue)

    layout[start[1]][start[0]] = 'S'
    layout[end[1]][end[0]] = 'E'


    while queue:
        # print('.', end='')
        # print()
        open_node = heapq.heappop(queue)[1]

        if open_node == end:
            path = utils.reconstruct_path(layout, prev, start, end)
            # maze.report(name='A*')
            # print(path)
            # print(prev)
            # print('hhhhhhhhhhhhhhhhhhhhhhhhhhh')

            return path

        neighbours = maze.get_neighbours(open_node)
        for neighbour in neighbours:
            if neighbour not in closed:
                distance_to_node = distance[open_node] + utils.get_distance(open_node, neighbour)
                distance_to_end = utils.get_distance(neighbour, end)

                if maze.layout[neighbour[1]][neighbour[0]] != 'X':
                    if (neighbour not in queue) or (distance_to_node < distance[neighbour]):
                        prev[neighbour] = open_node
                        distance[neighbour] = distance_to_node

                        if neighbour not in queue:
                            heapq.heappush(queue, (distance_to_node + distance_to_end, neighbour))
                        closed.append(neighbour)

        closed.append(open_node)
        # if open_node != start:
        #     layout[open_node[1]][open_node[0]] = 'O'

        timestep += 1

        # if put_on_a_show:
        #     maze.print_maze()
