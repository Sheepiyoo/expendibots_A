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