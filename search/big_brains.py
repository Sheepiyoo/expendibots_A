from game import get_grid_format
#  Node representation
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


def count_tokens(stack_list):
    total = 0
    for n, x, y in stack_list:
        total += n
    return total

# Checks a node - True if no black token remains
def goal_test(node):
    return len(node.board_dict['black']) == 0

# Implement heuristic function (Currently h(n) = number of black tokens) 
def heuristic(node):
    total = count_tokens(node.board_dict['black'])
    return total

# Implement A-star search
def search(initial_state):
    pass


def get_grid_format(board_dict):
    grid_format = {}
    for player in board_dict.keys():
        for stack in board_dict[player]:
            grid_format[(stack[1], stack[2])] = ''.join([player[0], str(stack[0])])
    return grid_format

#returns whether the token is white
def is_white(colour_n):
    player, n = colour_n
    if player == "w":
        return True
    return False

# returns a list of in-bound positions n spaces away from given x,y 
def possible_positions(x, y, n):
    positions = []
    if y+n < 8:
        positions.append((x, y+n))
    if x+n < 8:
        positions.append((x+n, y))
    if (x-n) >= 0:
        positions.append((x-n, y))
    if y-n >= 0:
        positions.append((x, y-n))
    print('the positions are', positions)
    return positions

# returns possible moves for a given stack
def get_possible_moves(stack, board):
    grid_board = get_grid_format(board)
    possible_moves = []
    x_pos = stack[1]
    y_pos = stack[2]
    possible_moves.append(["boom", (x_pos, y_pos), stack[0]])
    print(grid_board)
    for n in range(1, stack[0]+1):
        for (x, y) in possible_positions(x_pos, y_pos, n):
          if (x, y) in grid_board:
            if is_white(grid_board[(x, y)]):
              for i in range(1, stack[0]+1):
                possible_moves.append(["stack", (x, y), i])
          else:
              for i in range(1, stack[0]+1):
                  possible_moves.append(["move", (x, y), i])
    return possible_moves

