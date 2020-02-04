from collections import deque
import time
import bisect


def jaunt(channels, current_pos):  # TODO check edge cases, what if two channels are specified twice; what if
    jaunt_to = current_pos
    for i in channels:
        if current_pos == [i[0], i[1], i[2]]:
            jaunt_to = [i[3], i[1], i[2]]
        elif current_pos == [i[3], i[1], i[2]]:
            jaunt_to = [i[0], i[1], i[2]]
    return jaunt_to


# TODO: Change this whole monstrosity to a dictionary
# TODO can the world grid size be 0 0? should probable avoid a crash anyway
def next_position(world_grid, channels, current_pos, direction):
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
        next_point = jaunt(channels, current_pos)
    if next_point[1] >= len(world_grid):
        next_point = current_pos
    if next_point[2] >= len(world_grid[1]):
        next_point = current_pos
    if next_point[1] < 0:
        next_point = current_pos
    if next_point[2] < 0:
        next_point = current_pos
    return next_point


def find_path(tree, child):
    curr_parent = child
    path = list()
    while True:
        path.append(tree[str(curr_parent)])
        curr_parent = tree[str(curr_parent)]
        if curr_parent == [None]:
            break
    return path


def calculate_heuristic(end_state, current_state):
    current_cost = current_state[1]
    estimated_future_cost = (abs(current_state[0][0] - end_state[0])) \
                            + max(abs(current_state[0][1] - end_state[1]), abs(current_state[0][2] - end_state[2]))
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


def index_explored(a, value):
    i = bisect.bisect_left(a, value)
    if i != len(a) and a[i] == value:
        return i
    return -1


def breadth_first(world_grid, channels, start_state, end_state):
    cost = 0
    frontier = deque([])
    node = [[int(start_state[0]), int(start_state[1]), int(start_state[2])], cost]
    tree = {str(node): [None]}
    frontier_nodes = []
    # TODO: keep track of nodes in frontier as its own data structure
    if start_state == end_state:
        create_output(node, [node])
        return
    frontier.appendleft(node)
    frontier_nodes.append(node[0])
    explored = []
    actions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Jaunt']
    while True:
        if len(frontier) == 0:
            print("FAIL")
            return create_output(curr_node, ['FAIL'])
        curr_node = frontier.pop()
        temp = frontier_nodes.pop(0)
        bisect.insort(explored, curr_node[0])
        for action in actions:
            child = [next_position(world_grid, channels, curr_node[0], action),
                     curr_node[1] + 1]
            # print('action = {}'.format(action))#Suggest: this way you can have insertions in the middle of the string
            # if not in_frontier and not in_explored:
            # nodes_in_frontier = [n[0] for n in frontier]

            if child[0] not in frontier_nodes and index_explored(explored, child[0]) < 0:
                tree[str(child)] = curr_node
                if child[0] == end_state:
                    path = find_path(tree, child)
                    return create_output(child, path)
                frontier.appendleft(child)
                frontier_nodes.append(child[0])


def uniform_cost(world_grid, channels, start_state, end_state):
    cost = 0
    node = [[int(start_state[0]), int(start_state[1]), int(start_state[2])], cost]
    tree = {str(node): [None]}
    frontier = [node]
    explored = []
    actions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Jaunt']
    while True:
        if len(frontier) == 0:
            print(len(explored))
            return create_output(curr_node, ['FAIL'])
        curr_node = frontier[0]
        del frontier[0]
        if curr_node[0] == end_state:
            path = find_path(tree, curr_node)
            print(len(explored))
            return create_output(curr_node, path)
        bisect.insort(explored, curr_node[0])
        for action in actions:
            next_node = next_position(world_grid, channels, curr_node[0], action)
            if action == 'North' or action == 'South' or action == 'East' or action == 'West':
                cost = 10
            elif action == 'Jaunt':
                cost = abs(next_node[0] - curr_node[0][0])
            else:
                cost = 14
            child = [next_node, curr_node[1] + cost]
            # if not in_frontier and not in_explored:
            nodes_in_frontier = [n[0] for n in frontier]
            if child[0] not in nodes_in_frontier and index_explored(explored, child[0]) < 0:
                ind = len(frontier)
                for i in frontier:
                    if child[1] < i[1]:
                        ind = frontier.index(i)
                        break
                frontier.insert(ind, child)
                tree[str(child)] = curr_node
            elif child in nodes_in_frontier:
                index = frontier.index(child)
                if frontier > child[1]:
                    frontier.insert(index, child)
                    tree[str(child)] = curr_node


def a_star(world_grid, channels, start_state, end_state):
    cost = 0
    fn = 0
    node = [[int(start_state[0]), int(start_state[1]), int(start_state[2])], cost, fn]
    tree = {str(node): [None]}
    frontier = [node]
    explored = []
    actions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Jaunt']
    while True:
        if len(frontier) == 0:
            print(len(explored))
            return create_output(curr_node, ['FAIL'])
        curr_node = frontier[0]
        del frontier[0]
        if curr_node[0] == end_state:
            path = find_path(tree, curr_node)
            print(len(explored))
            return create_output(curr_node, path)
        bisect.insort(explored, curr_node[0])
        for action in actions:
            next_node = next_position(world_grid, channels, curr_node[0], action)
            if action == 'North' or action == 'South' or action == 'East' or action == 'West':
                cost = 10
            elif action == 'Jaunt':
                cost = abs(next_node[0] - curr_node[0][0])
            else:
                cost = 14
            child = [next_node, curr_node[1] + cost, fn]
            fn = calculate_heuristic(end_state, child)
            child = [next_node, curr_node[1] + cost, fn]
            # if not in_frontier and not in_explored:
            nodes_in_frontier = [n[0] for n in frontier]
            if child[0] not in nodes_in_frontier and index_explored(explored, child[0]) < 0:
                ind = len(frontier)
                for i in frontier:
                    if child[2] < i[2]:
                        ind = frontier.index(i)
                        break
                frontier.insert(ind, child)
                tree[str(child)] = curr_node
            elif child in nodes_in_frontier:
                index = frontier.index(child)
                if frontier > child[2]:
                    frontier.insert(index, child)
                    tree[str(child)] = curr_node


file_Input = open("input.txt")
lines = file_Input.readlines()
file_Input.close()

algorithm = lines[0].strip()
grid = lines[1].split()
width = int(grid[0])
height = int(grid[1])
# create world
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
    single_channel = [int(i) for i in single_channel]
    ch.append(single_channel)
    i = i + 1

#  create adjacency graph


st = time.time()
if algorithm == "BFS":
    breadth_first(world, ch, start, end)
elif algorithm == "UCS":
    uniform_cost(world, ch, start, end)
elif algorithm == "A*":
    a_star(world, ch, start, end)
print("it took {}".format(time.time() - st))
