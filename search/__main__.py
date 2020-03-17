import sys
import json

from search.util import print_move, print_boom, print_board
from search import game


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    print_board(game.get_grid_format(data) , "Before boom", compact=False)

    data = game.boom(4,7, data)

    print_board(game.get_grid_format(data), "After boom", compact=False)


if __name__ == '__main__':
    main()
