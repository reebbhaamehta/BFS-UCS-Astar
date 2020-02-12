from collections import deque
import time
import bisect
import heapq


# @profile
def jaunt(current_pos, channel_dict):
    jaunt_to_ = current_pos
    poss_jaunts = channel_dict[current_pos[0]]
    for i in poss_jaunts:
        if current_pos[1] == i[1] and current_pos[2] == i[2]:
            jaunt_to_ = list(i)
    return jaunt_to_


# TODO can the world grid size be 0 0? should probable avoid a crash anyway
# @profile
def next_position(world_grid, current_pos, direction, channel_dict):
    next_point = current_pos
    if direction == 'North':
        next_point = [current_pos[0], current_pos[1], current_pos[2] + 1]
    elif direction == 'Northeast':
        next_point = [current_pos[0], current_pos[1] + 1, current_pos[2] + 1]
    elif direction == 'East':
        next_point = [current_pos[0], current_pos[1] + 1, current_pos[2]]
    elif direction == 'Southeast':
        next_point = [current_pos[0], current_pos[1] + 1, current_pos[2] - 1]
    elif direction == 'South':
        next_point = [current_pos[0], current_pos[1], current_pos[2] - 1]
    elif direction == 'Southwest':
        next_point = [current_pos[0], current_pos[1] - 1, current_pos[2] - 1]
    elif direction == 'West':
        next_point = [current_pos[0], current_pos[1] - 1, current_pos[2]]
    elif direction == 'Northwest':
        next_point = [current_pos[0], current_pos[1] - 1, current_pos[2] + 1]
    elif direction == 'Jaunt':
        next_point = jaunt(current_pos, channel_dict)
    if next_point[1] >= len(world_grid):
        next_point = current_pos
    if next_point[2] >= len(world_grid[1]):
        next_point = current_pos
    if next_point[1] < 0:
        next_point = current_pos
    if next_point[2] < 0:
        next_point = current_pos
    return next_point


# @profile
def find_path(tree, child):
    curr_parent = child
    path = list()
    while True:
        path.append(tree[str(curr_parent)])
        curr_parent = tree[str(curr_parent)]
        if curr_parent == [None]:
            break
    return path


# @profile
def calculate_heuristic(end_state, current_state, channel_dict, explored_years, year_dict):
    current_cost = current_state[1]
    curr_year = current_state[0][0]
    curr_x = current_state[0][1]
    curr_y = current_state[0][2]
    jaunt_costs = [9999999]
    if end_state[0] == curr_year:
        estimated_future_cost = ((curr_x - end_state[1]) ** 2 + (curr_y - end_state[2]) ** 2) ** 0.5
    elif curr_year in channel_dict:  # if the goal is not in the current year but is in the path check if the current year is in the path
        for jaunts in channel_dict[curr_year]:  # for all jaunts find the distance to the closest jaunt location
            # if jaunts[0] not in explored_years:
            max_dist = (max(abs(curr_x - jaunts[1]), abs(curr_y - jaunts[2])))
            min_dist = (min(abs(curr_x - jaunts[1]), abs(curr_y - jaunts[2])))
            jaunt_costs.append((14 * min_dist) + (10 * (max_dist - min_dist)) + year_dict[curr_year])
        estimated_future_cost = min(jaunt_costs)
    else:
        estimated_future_cost = 99999999
    fn = current_cost + estimated_future_cost
    return fn


def create_output(current_node, path):
    file_output = open('output.txt', 'w')
    if path == ['FAIL']:
        file_output.write('FAIL')
    else:
        path.pop(len(path) - 1)
        path.reverse()
        path.append(current_node)
        file_output.write(str(current_node[1]))
        file_output.write('\n' + str(len(path)))
        prev_cost = 0
        for i in path:
            file_output.write(
                '\n' + str(i[0][0]) + ' ' + str(i[0][1]) + ' ' + str(i[0][2]) + ' ' + str(i[1] - prev_cost))
            prev_cost = i[1]
    file_output.close()


def get_index(find_in, value):
    i = bisect.bisect_left(find_in, value)
    if i != len(find_in) and find_in[i] == value:
        return i
    return -1


def add_node(pq, node, pq_dict):
    if tuple(node[2]) in pq_dict:
        pq_dict.pop(tuple(node[2]))
    pq_dict[tuple(node[2])] = node
    heapq.heappush(pq, node)


# @profile
def assign_costs_years(channel_dict, end_year):
    unvisited = []
    year_cost = {}
    for channel in channel_dict:
        if channel == end_year:
            cost = 0
        else:
            cost = 9999999
        unvisited.append([cost, channel])
        year_cost[channel] = cost
    unvisited.sort()
    while len(unvisited) != 0:
        current = unvisited[0]
        del unvisited[0]
        children = channel_dict[current[1]]
        for child in children:
            cost = abs(child[0] - current[1])
            child_q = [cost + current[0], child[0]]
            if year_cost[child_q[1]] >= 9999999:
                year_cost[child_q[1]] = child_q[0]
            y_unvisit = [i[1] for i in unvisited]
            if child_q[1] in y_unvisit:
                index = y_unvisit.index(child_q[1])
                if child_q[0] < unvisited[index][0]:
                    year_cost[child_q[1]] = child_q[0]
                    unvisited[index][0] = child_q[0]
                    unvisited.sort()
    return year_cost


def breadth_first(world_grid, start_state, end_state, channel_dict):
    cost = 0
    frontier = deque([])
    node = [[int(start_state[0]), int(start_state[1]), int(start_state[2])], cost]
    tree = {str(node): [None]}
    frontier_nodes = []
    if start_state == end_state:
        create_output(node, [node])
        return
    frontier.appendleft(node)
    frontier_nodes.append(node[0])
    explored = []
    actions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Jaunt']
    while True:
        if len(frontier) == 0:
            print("FAIL len(explored) = {}".format(len(explored)))
            return create_output(curr_node, ['FAIL'])
        curr_node = frontier.pop()
        frontier_nodes.pop(0)
        bisect.insort(explored, curr_node[0])
        for action in actions:
            child = [next_position(world_grid, curr_node[0], action, channel_dict),
                     curr_node[1] + 1]
            if child[0] not in frontier_nodes and get_index(explored, child[0]) < 0:
                tree[str(child)] = curr_node
                if child[0] == end_state:
                    print(len(explored))
                    path = find_path(tree, child)
                    return create_output(child, path)
                frontier.appendleft(child)
                frontier_nodes.append(child[0])


#  TODO: I dont think I am checking for removed nodes before poping them from pq. And I probably should be
def uniform_cost(world_grid, start_state, end_state, channel_dict):
    cost = 0
    counter = 0
    node = [cost, counter, [int(start_state[0]), int(start_state[1]), int(start_state[2])]]
    tree = {str([node[2], node[0]]): [None]}
    explored = []
    pq = []
    heap_dict = {}
    removed = []
    add_node(pq, node, heap_dict)
    actions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Jaunt']
    while True:
        if len(heap_dict) == 0:
            out_node = [curr_node[2], curr_node[0]]
            print(len(explored))
            return create_output(out_node, ['FAIL'])
        if get_index(explored, pq[0][2]) < 0:
            curr_node = heapq.heappop(pq)
            heap_dict.pop(tuple(curr_node[2]))
        else:
            heapq.heappop(pq)
            continue
        if curr_node[2] == end_state:
            out_node = [curr_node[2], curr_node[0]]
            path = find_path(tree, out_node)
            print(len(explored))
            return create_output(out_node, path)
        bisect.insort(explored, curr_node[2])
        for action in actions:
            next_node = next_position(world_grid, curr_node[2], action, channel_dict)
            if action == 'North' or action == 'South' or action == 'East' or action == 'West':
                cost = 10
            elif action == 'Jaunt':
                cost = abs(next_node[0] - curr_node[2][0])
            else:
                cost = 14
            counter += 1
            child = [curr_node[0] + cost, counter, next_node]
            if tuple(child[2]) not in heap_dict and get_index(explored, child[2]) < 0:
                add_node(pq, child, heap_dict)
                bisect.insort(removed, curr_node[2])
                tree[str([child[2], child[0]])] = [curr_node[2], curr_node[0]]
            elif tuple(child[2]) in heap_dict:
                if get_index(removed, child[2]) < 0:  # check if it is not in removed, it will return -1
                    q = heap_dict[tuple(child[2])]
                    if q[0] > child[0]:
                        tree[str([child[2], child[0]])] = [curr_node[2], curr_node[0]]
                        add_node(pq, child, heap_dict)
                        bisect.insort(removed, curr_node[2])


# @profile
def a_star(world_grid, start_state, end_state, channel_dict):
    cost, fn, counter = 0, 0, 0
    node = [fn, counter, [int(start_state[0]), int(start_state[1]), int(start_state[2])], cost]
    tree = {str([node[2], node[3]]): [None]}
    explored, pq, explored_years = [], [], set()
    pq_dict = {}
    add_node(pq, node, pq_dict)
    actions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Jaunt']
    year_dict = assign_costs_years(channel_dict, end_state[0])
    while True:
        if len(pq_dict) == 0:
            out_node = [curr_node[2], curr_node[3]]
            print(len(explored))
            return create_output(out_node, ['FAIL'])
        if get_index(explored, pq[0][2]) < 0:
            curr_node = heapq.heappop(pq)
            pq_dict.pop(tuple(curr_node[2]))
        else:
            heapq.heappop(pq)
            continue
        if curr_node[2] == end_state:
            out_node = [curr_node[2], curr_node[3]]
            path = find_path(tree, out_node)
            print(len(explored))
            return create_output(out_node, path)
        bisect.insort(explored, curr_node[2])
        explored_years.add(curr_node[2][0])
        for action in actions:
            next_node = next_position(world_grid, curr_node[2], action, channel_dict)
            if action == 'North' or action == 'South' or action == 'East' or action == 'West':
                cost = 10
            elif action == 'Jaunt':
                cost = abs(next_node[0] - curr_node[2][0])
            else:
                cost = 14
            counter += 1
            child = [fn, counter, next_node, curr_node[3] + cost]
            fn = calculate_heuristic(end_state, [child[2], child[3], child[0]], channel_dict, explored_years, year_dict)
            child = [fn, counter, next_node, curr_node[3] + cost]
            if tuple(child[2]) not in pq_dict and get_index(explored, child[2]) < 0:
                add_node(pq, child, pq_dict)
                tree[str([child[2], child[3]])] = [curr_node[2], curr_node[3]]
            elif tuple(child[2]) in pq_dict:
                if pq_dict[tuple(child[2])] is not None:  # re-eval
                    q = pq_dict[tuple(child[2])]
                    if q[0] > child[0]:
                        tree[str([child[2], child[3]])] = [curr_node[2], curr_node[3]]
                        add_node(pq, child, pq_dict)


file_Input = open("input.txt")
lines = file_Input.readlines()
file_Input.close()

algorithm = lines[0].strip()
grid = lines[1].split()
width = int(grid[0])
height = int(grid[1])

world = [[j for j in range(height)] for i in range(width)]

start = lines[2].rstrip().split()
start = [int(i) for i in start]

end = lines[3].rstrip().split()
end = [int(i) for i in end]

no_channels = int(lines[4].rstrip())

i = 0
ch = list()

while i < no_channels:
    single_channel = lines[5 + i].split()
    single_channel = [int(m) for m in single_channel]
    ch.append(single_channel)
    i = i + 1

channel_dict_global = {}

for i in ch:
    if i[0] in channel_dict_global:
        channel_dict_global[i[0]].append((i[3], i[1], i[2]))
    else:
        channel_dict_global[i[0]] = [(i[3], i[1], i[2])]
    if i[3] in channel_dict_global:
        channel_dict_global[i[3]].append((i[0], i[1], i[2]))
    else:
        channel_dict_global[i[3]] = [(i[0], i[1], i[2])]

st = time.time()
if algorithm == "BFS":
    breadth_first(world, start, end, channel_dict_global)
elif algorithm == "UCS":
    uniform_cost(world, start, end, channel_dict_global)
elif algorithm == "A*":
    a_star(world, start, end, channel_dict_global)
print("it took {}".format(time.time() - st))
