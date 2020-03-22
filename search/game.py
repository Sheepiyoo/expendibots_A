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

# Move a token
def move(stack, x, y, board_dict, n):
    grid_list = get_grid_format(board_dict)
    orig_n, orig_x, orig_y = stack

    #Check for valid number of tokens moved
    if (n > orig_n):
        raise Exception("""# Invalid move from ({}, {}) to ({}, {}):
                            Tried to move {} tokens when only {} available""".format(orig_x, orig_y, x, y, n, orig_n))

    #Check for valid direction
    elif (orig_y != y and orig_x != x):
        raise Exception("# Invalid move from ({}, {}) to ({}, {}): Not a cardinal direction".format(orig_x, orig_y, x, y))
    
    #Check for valid number of spaces moved
    elif (abs(orig_y - y) > n or abs(orig_x - x) > orig_n):
        raise Exception("# Invalid move from ({}, {}) to ({}, {}): Moved too many spaces".format(orig_x, orig_y, x, y))
    
    # Update original stack - 'lifting' the tokens
    grid_list[(orig_x, orig_y)] = "w" + str(orig_n - n)
    if (int(grid_list[(orig_x,orig_y)][1])) == 0:
        del(grid_list[(orig_x, orig_y)])

    #'Placing' the token
    #Check for existence of token
    if (x, y) in grid_list.keys():
        colour = grid_list[(x,y)][0]
        
        #Check for opponent piece
        if colour == "b":
            raise Exception("# Invalid move from ({}, {}) to ({}, {}): Opponent token present".format(orig_x, orig_y, x, y))
        
        #Add token to existing stack
        total = int(grid_list[(x,y)][1]) + n
        grid_list[(x,y)] = "w" + str(total)
    else:
        #Create a new token stack
        grid_list[(x,y)] = "w" + str(n)

    print("# Move {} pieces from {}, {} to {}, {}".format(n, orig_x, orig_y, x, y))
    return get_token_format(grid_list)


# Preprocessing for boom
def boom(stack, board_dict):
    _, x, y = stack
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
        print("# Removed token at" , x, y)

        #Recursive explosion
        for i in range(-1,2):
            for j in range(-1, 2):
                boom_recursive(x+i, y+j, grid_format)

    return