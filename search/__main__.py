import sys
import json
import time

from search.util import print_move, print_boom, print_board
from search import game
from search import big_brains as ai
from search.constants import *


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    
    """
    board = data
    print_board(game.get_grid_format(board) , "Start")
    board = game.move([1,0,1], [1,0,0], board)
    print_board(game.get_grid_format(board) , "Moved")
    board = game.move([1,0,1], [1,0,0], board)
    print_board(game.get_grid_format(board) , "Moved")
    """
    start = time.time()
    
    print(data)
    board = data
    print_board(game.get_grid_format(board) , "Start")

    solution = ai.search(data)
    print("# solution",solution)
    

    #ai.breadth_first_tree_traversal(solution)
        
    for action, stack_from, stack_to in solution:
        if action == "move" or action == "stack":
            board = game.move(stack_from, stack_to, board)
            if DEBUG: print_board(game.get_grid_format(board))
            else: print_move(stack_to[N_TOKENS], stack_from[X_POS], stack_from[Y_POS], stack_to[X_POS], stack_to[Y_POS])

        if action == "boom":
            board = game.boom(stack_from, board)
            if DEBUG: print_board(game.get_grid_format(board))
            else: print_boom(stack_from[X_POS], stack_from[Y_POS])
            pass
    print("# length of solution ", len(solution))
    print("# Execution time: ", time.time() - start)

if __name__ == '__main__':
    main()
