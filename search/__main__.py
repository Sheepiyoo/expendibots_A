import sys
import json

from search.util import print_move, print_boom, print_board
from search import game


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence

    print_board(game.get_grid_format(data) , "Original", compact=False)
    
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


if __name__ == '__main__':
    main()
