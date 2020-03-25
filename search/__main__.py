import sys
import json

from search.util import print_move, print_boom, print_board
from search import game
from search import big_brains as ai


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    root = ai.Node(data, 0, None, None)
    print(root)

    print(data)
    print_board(game.get_grid_format(data) , "Original", compact=False)

    tree = ai.search(data)

    ai.breadth_first_tree_traversal(tree)

    """
    for i in range(len(data["white"])):
        possible_moves = ai.get_possible_moves(data["white"][i], data)
        print(possible_moves)
        for move in possible_moves:
            new_state = ai.state_after_move(data["white"][i], data, move)
            print_board(game.get_grid_format(new_state), str(move), compact=False)
    """

    #data = game.move(data["white"][0], 0, 0, data, 1)

    #print_board(game.get_grid_format(data) , "Move 0,1 to 0,0", compact=False)

    #moved = ai.Node(data, 1, ["move", (0,1), (0,0), 1], root)

    #print(moved)

    """
    data = game.move(data["white"][0], 0, 0, data, 1)
    data["white"].sort()
    print(data["white"])
    print_board(game.get_grid_format(data) , "Move 0,1 to 0,0", compact=False)
    
    data = game.move(data["white"][0], 1, 0, data, 1)
    print(data["white"])
    
    print_board(game.get_grid_format(data) , "Move 0,0 to 1,0", compact=False)
    data = game.move(data["white"][0], 3, 0, data, 1)
    
    print_board(game.get_grid_format(data) , "Move 1,0 to 3,0", compact=False)


    print_board(game.get_grid_format(data) , "Before boom", compact=False)
    data = game.boom(data["white"][0], data)
    
    print_board(game.get_grid_format(data), "After boom", compact=False)
    """

if __name__ == '__main__':
    main()
