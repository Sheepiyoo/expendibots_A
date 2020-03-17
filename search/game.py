# Converts from (x,y) as keys to "white", "black" as keys
# {(x, y): "wn"} --> {"white": [n, x, y]}

def get_token_format(grid_dict):
    token_format = {"white":[], "black": []}
    for coordinate in grid_dict.keys():
        x, y = coordinate
        player, n = grid_dict[coordinate]

        if player == 'w':
            token_format["white"].append([int(n), x, y])
        elif player == 'b':
            token_format["black"].append([int(n), x, y])

    return token_format

# Converts from "white", "black" as keys to (x,y) as keys 
# {"white": [n, x, y]} --> {(x, y): "wn"}       
def get_grid_format(board_dict):
    grid_format = {}
    for player in board_dict.keys():
        for stack in board_dict[player]:
            grid_format[(stack[1], stack[2])] = ''.join([player[0], str(stack[0])])
    
    return grid_format

def move(token, x, y, board_dict, n):
    if (token[0] - n) == 0:
        list = get_grid_format(board_dict)
        del(list[(token[1], token[2])])
    if (x, y) in list:
        total = int(list[(x,y)][1]) + n
        list[(x,y)] = "w" + str(total)
    else:
        list[(x,y)] = "w" + str(n)
    return get_token_format(list)


# Preprocessing for boom
def boom(x, y, board_dict):
    grid_format = get_grid_format(board_dict)
    boom_recursive(x, y, grid_format)
    return get_token_format(grid_format)


def boom_recursive(x, y, grid_format):
    #Check bounds
    if not (0 <= x < 8 and 0 <= y < 8):
        return
    
    #If a token is present, explode!        
    if (x, y) in grid_format.keys():
        del(grid_format[(x,y)])
        
        #Debug line
        print("removed token at" , x, y)

        #Recursive explosion
        for i in range(-1,2):
            for j in range(-1, 2):
                boom_recursive(x+i, y+j, grid_format)

    return