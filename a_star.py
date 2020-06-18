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

    # print('constraints')
    # print(constraints)
    

    while queue:
        # print('.', end='')
        # print()
        # print('x'*200, 'cyklus +1')
        # print(timestep)
        open_node = heapq.heappop(queue)[1]


        if open_node == end:
            path = utils.reconstruct_path(layout, prev, start, end, waits)
            # maze.report(name='A*')
            print(path, ' a star output, konec')
            # print('/'*200)
            # print(path)
            return path
       
        if constraints:
            current_constraint = utils.import_current_constraints(constraints, timestep)

        neighbours = maze.get_neighbours(open_node)
        # print('queue')
        # print(queue)
        # print('prev')
        # print(prev)
        # print('neighbours')
        # print(neighbours)
        # print('currently at')
        # print(open_node)

        for neighbour in neighbours:
            if neighbour not in closed:
                distance_to_node = distance[open_node] + utils.get_manhattan_distance(open_node, neighbour)
                distance_to_end = utils.get_manhattan_distance(neighbour, end)

                if constraints:
                    occupied = utils.is_occupied(neighbour, current_constraint)
                    # print('constraints')
                    # print(constraints)
                else:
                    occupied = False
                
                if occupied:
                    print('occupied')
                    print(occupied)

                if maze.layout[neighbour[1]][neighbour[0]] != 'X':
                    if not occupied:
                        if (neighbour not in queue) or (distance_to_node < distance[neighbour]):
                            prev[neighbour] = open_node
                            distance[neighbour] = distance_to_node

                            if neighbour not in queue:
                                heapq.heappush(queue, (distance_to_node + distance_to_end, neighbour, timestep))
                            closed.append(neighbour)
                    elif occupied:
                        print('wait added', neighbour)
                        if neighbour not in waits:
                            waits.append(neighbour)
                    
        # if len(queue) == 1 and queue[0][1] == open_node:
        # if len(queue) == 1 and queue[0][1] == open_node:
            # print('TED CEKAM' * 100)
            # waits.append(open_node)
        closed.append(open_node)
        # print('queue at end')
        # print(queue)
        # print('closed')
        # print(closed)
        
        # if open_node != start:
        #     layout[open_node[1]][open_node[0]] = 'O'

        timestep += 1

        # if put_on_a_show:
        #     maze.print_maze()
