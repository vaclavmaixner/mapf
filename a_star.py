import utils
import heapq


def run_a_star(maze, layout, start, end, put_on_a_show, constraints):
    queue = []
    closed = []
    prev = {}
    distance = {}

    timestep = 0

    heapq.heappush(queue, (0, start, timestep))
    distance[start] = 0

    layout[start[1]][start[0]] = 'S'
    layout[end[1]][end[0]] = 'E'

    current_constraint = []

    waits = []

    while queue:
        open_node = heapq.heappop(queue)[1]

        if open_node == end:
            path = utils.reconstruct_path(layout, prev, start, end, waits)
            return path

        if constraints:
            current_constraint = utils.import_current_constraints(
                constraints, timestep)

        neighbours = maze.get_neighbours(open_node)

        for neighbour in neighbours:
            if neighbour not in closed:
                distance_to_node = distance[open_node] + \
                    utils.get_manhattan_distance(open_node, neighbour)
                distance_to_end = utils.get_manhattan_distance(neighbour, end)

                if constraints:
                    occupied = utils.is_occupied(neighbour, current_constraint)
                else:
                    occupied = False

                if maze.layout[neighbour[1]][neighbour[0]] != 'X':
                    if not occupied:
                        if (neighbour not in queue) or (distance_to_node < distance[neighbour]):
                            prev[neighbour] = open_node
                            distance[neighbour] = distance_to_node

                            if neighbour not in queue:
                                heapq.heappush(
                                    queue, (distance_to_node + distance_to_end, neighbour, timestep))
                            closed.append(neighbour)
                    elif occupied:
                        if neighbour not in waits:
                            waits.append(neighbour)

        closed.append(open_node)

        timestep += 1
