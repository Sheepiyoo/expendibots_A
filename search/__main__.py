import sys
import json

from search.util import print_move, print_boom, print_board
import search.game

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    gameboard = search.game.Board(data)
    print_board(gameboard.grid_dict, "Before boom", compact=False)
    print(gameboard.board_dict)
    print(gameboard.grid_dict)

    gameboard.boom(1,0)

    print_board(gameboard.grid_dict, "After boom", compact=False)
    print(gameboard.board_dict)
    print(gameboard.grid_dict)

    #Should we use dictionary with coordinates as keys, or players as keys to implement MOVE and BOOM?

if __name__ == '__main__':
    main()
