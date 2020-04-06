from search.game import get_grid_format, boom, move
from search.constants import *
from search.util import *
import search.hotspot as hotspot
import traceback
import heapq

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
        self.f = self.heuristic + self.path_cost

    def __str__(self):
        return """
# State: {}
# Path Cost: {}
# Heuristic: {}
# Action: {}
# Parent: {}
# Children: {}
""".format(str(self.board_dict), str(self.path_cost), str(self.heuristic), str(self.action), hex(id(self.parent)), [hex(id(child)) for child in self.children])
    
    def __lt__(self, other):
        #if self.f == other.f: return self.path_cost < other.path_cost
        return self.f < other.f

def count_tokens(stack_list):
    total = 0
    for n, x, y in stack_list:
        total += n
    return total

# Checks a node - True if no black token remains
def goal_test(node):
    return len(node.board_dict['black']) == 0

def heuristic(node):
    # Best of n stack distance
    if len(node.board_dict["white"]) > 0:
        best_stack = max([stack[N_TOKENS] for stack in node.board_dict['white']])
    else:
        best_stack = 1

    distances = []
    
    for stack in node.board_dict["black"]:
        distances.append(min_distance_from_stack(stack, node.board_dict["white"]))
    
    #distances.sort()    
    return sum(distances)//best_stack #(max(0.01, len(node.board_dict["white"])))# * best_stack) #best_stack 


def min_distance_from_chunk(chunk, stack_list):
    min_distance = BOARD_SIZE*2

    for stack in chunk:
        min_distance = min(min_distance, min_distance_from_stack(stack, stack_list))
    
    return min_distance

def min_distance_from_stack(source, stack_list):
    # Minimum distance from a black stack to one of the white stacks
    min_distance = BOARD_SIZE*2
    for i in range(len(stack_list)):
        h_dist = hamming_distance(source, stack_list[i]) - 1
        #c_dist = chess_distance(source, stack_list[i]) - 1
        
        min_distance = min(min_distance, h_dist)

    return min_distance

def hamming_distance(stack1, stack2):
    # Chess board distance as booming can take surrounding 9 squares
    return abs(stack1[X_POS]-stack2[X_POS]) + abs(stack1[Y_POS]-stack2[Y_POS])

def get_chunks(board_dict):
    chunks = [] 
    grid_format = get_grid_format(board_dict)
    grid_copy = grid_format.copy()

    for (x,y) in grid_copy:
        chunk = []
        chunk_recursive(x, y, grid_format, chunk)
        if len(chunk) != 0:
          chunks.append(chunk)
    return chunks


def chunk_recursive(x, y, grid_format, chunk):
    #Check bounds
    if not (0 <= x < 8 and 0 <= y < 8):
        return
    
    #If a token is present, explode!        
    if (x, y) in grid_format.keys():
        chunk.append([int(grid_format[(x,y)][1:]), x, y])
        del(grid_format[(x,y)])

        #Recursive explosion
        for i in range(-1,2):
            for j in range(-1, 2):
                chunk_recursive(x+i, y+j, grid_format, chunk)
    else:
      return
    return    

#######################################################################################

def dict_to_set(board_dict):
    new_dict = set()
    for i in board_dict["white"]:
        new_dict.add(tuple([0] + i))

    for i in board_dict["black"]:
        new_dict.add(tuple([1] + i))
    
    return frozenset(new_dict)

# Implement A-star search
def search(initial_state):
    goal_found = False
    solution = []

    start_node = Node(initial_state, 0, None, None)
    
    # Node queue
    nextmoves_list = []
    heapq.heappush(nextmoves_list,start_node)

    # Collection of states
    explored_states = set()

    while(len(nextmoves_list) > 0):
        curr_node = heapq.heappop(nextmoves_list)    # Remove best node from open list
        if goal_test(curr_node):
            goal_found = True
            break
        
        if dict_to_set(curr_node.board_dict) in explored_states: continue

        explored_states.add(dict_to_set(curr_node.board_dict))
        
        # Prune guaranteed losses
        if count_tokens(curr_node.board_dict["white"]) == 0: continue

        elif curr_node.action != None and curr_node.action[0] == "boom":
            # Check if possible to win at all
            min_white_needed = len(hotspot.get_all_hotspots(curr_node.board_dict))
            num_white = count_tokens(curr_node.board_dict["white"])
                    
            # If guarantee loss, don't bother generating children
            if num_white < min_white_needed: continue

        # For each curr_node find possible moves and heuristic values of each move
        generate_children(curr_node)

        # Create children nodes for each move and add them to the open_list
        for child in curr_node.children:
            # Check if we have explored this state already
            if dict_to_set(child.board_dict) in explored_states: continue

            # Reached the goal
            if goal_test(child):
                curr_node = child
                goal_found = True
                break
            
            # if path to child is shorter than previous path to child 
            heapq.heappush(nextmoves_list, child)
 
        if goal_found: break
        
    # If searched and no solution found
    if goal_found == False:
        print("# No solution")
        raise Exception("No solution possible")
        return
        
    # Reconstruct solution by tracing back parents from curr_node (Thanks Emily :D )
    while(curr_node.parent != None):
        solution.insert(0, curr_node.action)
        curr_node = curr_node.parent

    return solution 

#returns whether the token is white
def is_white(colour_n):
    player = colour_n[0]
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
    x_pos, y_pos = stack_from[X_POS],  stack_from[Y_POS]
    possible_actions.append(["boom", stack_from, stack_from])
    #print(grid_board)
    
    # for each possible stack of n tokens 
    for n in range(1, stack_from[N_TOKENS]+1):
        # print(n, "this is n")
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
    #print(possible_actions)
    return possible_actions

# Given a node, generate all possible children from that node
def generate_children(parent_node):
    for stack in parent_node.board_dict["white"]:
        actions = get_possible_actions(stack, parent_node.board_dict)
        #print('possible actions',actions)
        for action in actions:
            try:
                next_state = state_after_move(stack, parent_node.board_dict, action)
                child_node = Node(next_state,
                                parent_node.path_cost + 1,
                                action,
                                parent_node)
            except:
                traceback.print_exc()
                print("Bug - Crashing program")
                print(parent_node, move, stack)
                exit()
            parent_node.children.append(child_node)
    return

# Generates the board_state after a move, without modifiying the original state
def state_after_move(stack, board_dict, action):
    if action[ACTION] == "boom":
        try:
            board_dict = boom(stack, board_dict)
        except Exception as e:
            print(e)
            print("Tried to execute: boom({}, {}) ".format(stack, board_dict))
            raise Exception("Move invalid")
    elif action[ACTION] == "move":
        try:
            board_dict = move(stack, action[TO], board_dict)
        except Exception as e:
            print(str(e))
            print("Tried to execute: move({}, {}, {}, {}, {}) ".format(stack, action[TO][X_POS], action[TO][Y_POS], board_dict, action[TO][N_TOKENS]))
            raise Exception("Move invalid")
    else:
        raise Exception("state_after_move: Invalid action")
    
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

