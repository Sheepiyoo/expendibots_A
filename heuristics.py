# Implement heuristic function (Currently h(n) = number of black tokens) 
def heuristic1(node):
    # Best of n chunk distance
    if len(node.board_dict["white"]) > 0:
        best_stack = max([stack[N_TOKENS] for stack in node.board_dict['white']])
    else:
        best_stack = 1

    chunk_list = get_chunks({"black": node.board_dict["black"]})
    distances = []
    
    for chunk in chunk_list:
        distances.append(min_distance_from_chunk(chunk, node.board_dict["white"]))
    
    distances.sort()
    return sum(distances)//best_stack #[:len(node.board_dict["white"])]

def heuristic2(node):
    # Number of black tokens remaining
    return count_tokens(node.board_dict["black"])

def heuristic3(node):
    # Best of n stack distance
    if len(node.board_dict["white"]) > 0:
        best_stack = max([stack[N_TOKENS] for stack in node.board_dict['white']])
    else:
        best_stack = 1

    distances = []
    
    for stack in node.board_dict["black"]:
        distances.append(min_distance_from_stack(stack, node.board_dict["white"]))
    
    distances.sort()    
    return sum(distances)//best_stack

def heuristic4(node):
    # Total minimum stack distance
    if len(node.board_dict["white"]) > 0:
        best_stack = max([stack[N_TOKENS] for stack in node.board_dict['white']])
    else:
        best_stack = 1

    chunk_list = get_chunks({"black": node.board_dict["black"]})
    distances = []
    
    for chunk in chunk_list:
        distances.append(min_distance_from_chunk(chunk, node.board_dict["white"]))
    
    return sum(distances)//best_stack

def heuristic5(node):
    # Not admissible because of heuristic 2
    #num_black = len(node.board_dict["black"])
    #num_black = len(get_chunks({"black": node.board_dict["black"]}))
    #num_white = len(get_chunks({"white": node.board_dict["white"]}))

    #if num_black <= num_white:
    #    return heuristic3(node)
    #else:
    #    return heuristic3(node)
    return heuristic3(node)