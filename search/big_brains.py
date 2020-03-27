from search.game import get_grid_format, boom, move
from search.constants import *

# Node representation
# board_dict: Token arrangement on board
# path_cost: Total path cost to the node so far = depth
# heuristic: Heuristic at current node
# action: What action led to that
# parent: Parent node
class Node:
    def __init__(self, board_dict, path_cost, action, parent):
        self.board_dict = board_dict
        self.path_cost = path_cost
        self.action = action
        self.parent = parent
        self.children = []
        self.heuristic = heuristic(self)

    def __str__(self):
        return """
# State: {}
# Path Cost: {}
# Heuristic: {}
# Action: {}
# Parent: {}
# Children: {}
""".format(str(self.board_dict), str(self.path_cost), str(self.heuristic), str(self.action), hex(id(self.parent)), [hex(id(child)) for child in self.children])


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
    goal_found = False
    solution = []
    start_node = Node(initial_state, 0, None, None)
    final_node = None
    
    # Node queue
    nextmoves_list = []
    explored_list = []

    # Collection of states
    explored_states = []

    nextmoves_list.append(start_node)

    while(len(nextmoves_list) > 0):
        print(nextmoves_list)
        curr_node = nextmoves_list.pop(0)    # Remove best node from open list
        if goal_test(curr_node):
            print("# GOAL FOUND: BIG BRAINZ")
            break

        # Check if we have explored this state already
        if curr_node.board_dict in explored_states: continue

        # For each curr_node find possible moves and heuristic values of each move
        generate_children(curr_node)

        # Create children nodes for each move and add them to the open_list
        for child in curr_node.children:
            if goal_test(child):
                # reached the goal
                curr_node = child
                goal_found = True
                final_node = child
                break
            
            nextmoves_list.append(child)

        if goal_found:
            print("# GOAL FOUND: BIG BRAINZ")
            break

        # sort open_list
        nextmoves_list.sort(key = lambda x: x.heuristic)        # Can add path cost to get A star
        explored_list.append(curr_node)   # Insert into closed list
        explored_states.append(curr_node.board_dict)

    # Reconstruct solution by tracing back parents from curr_node (Thanks Emily :D )
    while(curr_node.parent != None):
        solution.insert(0, curr_node.action)
        curr_node = curr_node.parent
    return solution #for debugging purposes - change to return 'solution' after


#returns whether the token is white
def is_white(colour_n):
    player, n = colour_n
    if player == "w":
        return True
    return False

# returns a list of in-bound positions n spaces away from given x,y
def possible_positions(x, y, n):
    positions = []
    if y+n < BOARD_SIZE:
        positions.append((x, y+n))
    if x+n < BOARD_SIZE:
        positions.append((x+n, y))
    if (x-n) >= 0:
        positions.append((x-n, y))
    if y-n >= 0:
        positions.append((x, y-n))
    #print('the positions are', positions)
    return positions

# returns possible moves for a given stack
# Each action has the format: ["action", origin, target, n_tokens]
def get_possible_actions(stack_from, board):
    grid_board = get_grid_format(board)
    possible_actions = []
    #n_original = stack
    x_pos, y_pos = stack_from[X_POS],  stack_from[Y_POS]
    possible_actions.append(["boom", stack_from, stack_from])
    #print(grid_board)
    
    # for each possible stack of n tokens 
    for n in range(1, stack_from[N_TOKENS]+1):
        print(n, "this is n")
        # for each possible position from given position
        for (x, y) in possible_positions(stack_from[X_POS], stack_from[Y_POS], n):

            # if a stack already exists on the board, add the stack
            if (x, y) in grid_board:
                if is_white(grid_board[(x, y)]):
                    for i in range(1, stack_from[0]+1):
                        stack_to = [i, x, y]
                        possible_actions.append(["move", stack_from, stack_to])
                
            else:
                for i in range(1, stack_from[0]+1):
                    stack_to = [i, x, y]
                    possible_actions.append(["move", stack_from, stack_to])
    print(possible_actions)
    return possible_actions

# Given a node, generate all possible children from that node
def generate_children(parent_node):
    for stack in parent_node.board_dict["white"]:
        actions = get_possible_actions(stack, parent_node.board_dict)
        print('possible actions',actions)
        for action in actions:
            try:
                child_node = Node(state_after_move(stack, parent_node.board_dict, action),
                                parent_node.path_cost + 1,
                                action,
                                parent_node)
            except:
                print("Bug - Crashing prgoram")
                print(parent_node, move, stack)
                exit()
            parent_node.children.append(child_node)
    return

# Generates the board_state after a move, without modifiying the original state
def state_after_move(stack, board_dict, action):
    if action[ACTION] == "boom":
        try:
            board_dict = boom(stack, board_dict)
        except:
            print("Tried to execute: boom({}, {}) ".format(stack, board_dict))
            raise Exception("Move invalid")
    elif action[ACTION] == "move":
        try:
            board_dict = move(stack, action[TO], board_dict)
        except:
            print("Tried to execute: move({}, {}, {}, {}, {}) ".format(stack, action[TO][X_POS], action[TO][Y_POS], board_dict, action[TO][N_TOKENS]))
            raise Exception("Move invalid")
    else:
        raise Exception("state_after_move: Invalid action")
    #print(board_dict)
    return board_dict

# Debugging tool: Print out all nodes of the tree
def breadth_first_tree_traversal(root):
    checked = []
    checked.append(root)
    count = 0
    while(len(checked) > 0):
        count += 1
        current = checked.pop(0)
        print(current)

        for child in current.children:
            checked.append(child)
    
    print("# Nodes explored: ", count)
    return
