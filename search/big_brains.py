# Node representation
class Node:
    def __init__(self, board_dict, path_cost, heuristic, action, parent):
        self.state = board_dict
        self.path_cost = path_cost
        self.heuristic = heuristic
        self.action = action
        self.parent = parent
        self.children = []

    def __str__(self):
        return """
# State: {}
# Path Cost: {}
# Heuristic: {}
# Action: {}
# Parent: {}
# Children: {}
""".format(str(self.state), str(self.path_cost), str(self.heuristic), str(self.action), hex(id(self.parent)), [hex(id(child)) for child in self.children])

# Checks a node - True if no black token remains
def goal_test(node):
    # Need to implement token counter

    return len(node.board_dict['black']) == 0

# Implement heuristic function (Currently h(n) = number of black tokens) 
def heuristic(node):
    # Need to implement token counter

    return len(node.board_dict['black'])

# Implement A-star search
def search(initial_state):
    pass

def is_white(colour_n):
    player, n = colour_n
    if player == "w":
        return True
    return False

def possible_positions(x, y, n):
    positions = []
    if y+n < 9:
        positions.append((x, y+n))
    if x+n < 9:
        positions.append((x+n, y))
    if (x-n) > 0:
        positions.append((x-n, y))
    if y-n > 0:
        positions.append((x, y-n))
    return positions


def get_possible_moves(stack, board):
    grid_board = get_grid_format(board)
    possible_moves = []
    x_pos = stack[1]
    y_pos = stack[2]
    possible_moves.append(["boom", (x_pos, y_pos), stack[0]])
    for n in range(1, stack[0]):
        for (x, y) in possible_positions(x_pos, y_pos, n):
            if is_white(grid_board[(x, y)]):
                possible_moves.append(["stack", x, y])
            else:
                for i in range(1, n):
                    possible_moves.append(["move", (x, y), i])
    return possible_moves
