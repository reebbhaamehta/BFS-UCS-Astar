"""
function GRAPH-SEARCH(problem) return a solution or failure
frontier <- MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
explored_set <- empty
loop do
if EMPTY?(frontier) then return failure
node <- REMOVE-FIRST(frontier)
if problem.GOAL-TEST applied to node.STATE succeeds
then return SOLUTION(node)
explored_set <- INSERT(node, explored_set)
for each new_node in EXPAND(node, problem) do
if NOT(MEMBER?(new_node, frontier)) and
NOT(MEMBER?(new_node, explored_set))
then frontier <- INSERT(new_node, frontier
"""

from collections import deque


def add_node_path(element, input_list):
    return [element] + input_list


def get_root(path):
    return path


def get_path(input_list):
    i = 0
    out_list = []
    for i in input_list:
        #print[i]
        out_list.append(get_root(i))
    return out_list


def jaunt(channels, current_pos):  # TODO check edge cases, what if two channels are specified twice; what if
    jaunt_to = current_pos
    for i in channels:
        if current_pos == [i[0], i[1], i[2]]:
            print('jaunt possible#1')
            jaunt_to = [i[3], i[1], i[2]]
        elif current_pos == [i[3], i[1], i[2]]:
            print('jaunt possible#2')
            jaunt_to = [i[0], i[1], i[2]]
    return jaunt_to


# TODO can the world grid size be 0 0? should probable avoid a crash anyway
def next_position(world_grid, channels, current_pos, direction):  # TODO: Change this whole monstrosity to a dictionary
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


def breadth_first(world, channels, start_state, end_state, ):
    cost = 0
    frontier = deque([])
    node = [[int(start_state[0]), int(start_state[1]), int(start_state[2])], cost]
    # TODO: add a path tree for the path.
    path = add_node_path(node, [])
    print(path)
    if start_state == end_state:
        create_output(node)
        return
    frontier.appendleft(node)
    explored = []
    actions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Jaunt']
    while True:
        if len(frontier) == 0:
            no_solution = 'FAIL'
            print(no_solution)
            return create_output(no_solution)
        curr_node = frontier.pop()
        path = add_node_path(curr_node, path)
        cost += 1
        explored.append(curr_node[0])

        for action in actions:
            child = [next_position(world, channels, curr_node[0], action),
                     curr_node[1] + 1]  # TODO: make cost a number (removing [] parenthesis)

            # print('action = {}'.format(action))#Suggest: this way you can have insertions in the middle of the string

            # if not in_frontier and not in_explored:
            nodes_in_frontier = [n[0] for n in frontier]

            if child[0] not in explored and child[0] not in nodes_in_frontier:
                if child[0] == end_state:
                    solution_found = 'Got something'
                    path = get_path(child[0])
                    print(solution_found, child, path)
                    return create_output(solution_found)
                frontier.appendleft(child)
                path = add_node_path(child, path)

    return


def uniform_cost(world, channels, start_state, end_state, ):
    cost = 0
    frontier = deque([])
    node = [[int(start_state[0]), int(start_state[1]), int(start_state[2])], cost]
    frontier.appendleft(node)
    explored = []
    # TODO: add a path tree for the path.
    path = add_node_path(node, [])
    print(path)
    actions = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest', 'Jaunt']
    while True:
        if len(frontier) == 0:
            no_solution = 'FAIL'
            print(no_solution)
            return create_output(no_solution)
        curr_node = frontier.pop()
        if curr_node == end_state:
            solution_found = 'Got something'
            print(solution_found, curr_node)
            return create_output(solution_found)
        path = add_node_path(curr_node, path)
        explored.append(curr_node[0])
        for action in actions:
            child = [next_position(world, channels, curr_node[0], action),
                     curr_node[1] + 1]  # TODO: correct the cost for ucs
            path = add_node_path(child, path)
            # print('action = {}'.format(action))#Suggest: this way you can have insertions in the middle of the string

            # if not in_frontier and not in_explored:
            nodes_in_frontier = [n[0] for n in frontier]

            if child[0] not in explored and child[0] not in nodes_in_frontier:
                frontier.appendleft(child)#TODO: insert in correct location
            #elif chi

    return


def a_star():
    return


def create_output(out_list):
    file_output = open('output.txt', 'w')
    file_output.write("You know how it goes. Slow learning" + '\n')
    file_output.write(str(out_list))
    file_output.close()


lines = list()
file_Input = open("input.txt")
lines = file_Input.readlines()
file_Input.close()
# with open('input.txt') as file_Input:
#    lines = file_Input.readlines()

algorithm = lines[0].strip()
grid = lines[1].split()
width = int(grid[0])
height = int(grid[1])
# create world
world = [[0 for j in range(height)] for i in range(width)]
# populate world with valid possible positions

for j in range(height):
    for i in range(width):
        world[i][j] = [i, j]

start = lines[2].rstrip().split()
start[0] = int(start[0])
start[1] = int(start[1])
start[2] = int(start[2])
end = lines[3].rstrip().split()
end[0] = int(end[0])
end[1] = int(end[1])
end[2] = int(end[2])
no_channels = int(lines[4].rstrip())

i = 0
ch = list()

while i < no_channels:
    single_channel = lines[5 + i].split()
    single_channel = [int(i) for i in single_channel]
    ch.append(single_channel)
    i = i + 1
# print(ch)

if algorithm == "BFS":
    breadth_first(world, ch, start, end)
elif algorithm == "UCS":
    uniform_cost(world, ch, start, end)
elif algorithm == "A*":
    breadth_first(world, ch, start, end)
    # a_star()
