import random
import json
from search.util import print_board
from search.game import get_grid_format

def run():
    BOARD_SIZE = 8
    MAX_NUM_WHITE = 12
    MAX_NUM_BLACK = 12

    MAX_STACK_WHITE = 12
    MAX_STACK_BLACK = 12

    data = {"white": [],
            "black": []}

    num_stack_white = random.randint(1, MAX_STACK_WHITE)
    num_stack_black = random.randint(1, MAX_STACK_BLACK)

    occupied = []

    for stack in range(num_stack_white):
        if MAX_NUM_WHITE <= 0: break

        n = random.randint(1, min(2, MAX_NUM_WHITE))
        x = random.randint(0, 7)
        y = random.randint(0, 7)

        if (x, y) not in occupied:
            occupied.append((x,y))
            data["white"].append([n, x, y])
            MAX_NUM_WHITE -= n

    for stack in range(num_stack_black):
        if MAX_NUM_BLACK <= 0: break

        n = random.randint(1, min(3, MAX_NUM_BLACK))
        x = random.randint(0, 7)
        y = random.randint(0, 7)

        if (x, y) not in occupied:
            occupied.append((x,y))
            data["black"].append([n, x, y])
            MAX_NUM_BLACK -= n

    print(data)
    print_board(get_grid_format(data))

    #accepted = input("Accept this arrangement? (y/n): \n")

    if True:
        json_form = json.dumps(data)
        
        with open("test.json", 'w') as f:
            f.write(json_form)

        print("Board accepted")

    else:
        print("Board rejected")