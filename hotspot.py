def get_grid_format(board_dict):
    grid_format = {}
    for player in board_dict.keys():
        for stack in board_dict[player]:
            grid_format[(stack[1], stack[2])] = ''.join([player[0], str(stack[0])])
    return grid_format

def token_positions(token_form, colour):
  copy_tokens = token_form.copy()
  #del copy_tokens["white"]
  black_tokens = copy_tokens
  return get_grid_format(black_tokens)

#this doesn't take into account chunks
def get_good_pos(board_dict):
    priority_dict = {}
    b_tokens = token_positions(board_dict, "black")
    for token in board_dict["black"]:
        poss_positions = possible_bomb_positions(token[1], token[2], 1)
      
        for position in poss_positions:
          if position in b_tokens:
            pass
          else:
              if position in priority_dict : # and also if they're not part of the same bunch
                  priority_dict[position] += 1

              else:
                  priority_dict[position] = 1
    d2 = {}
    for k in sorted(priority_dict, key=priority_dict.get, reverse=True):
      d2[k] = priority_dict[k]
    return d2

def possible_bomb_positions(x, y, n):
    positions = []
    if y+n < 8:
        positions.append((x, y+n))
        if x+n < 8:
          positions.append((x+n, y+n))
        if x-n >=0:
          positions.append((x-n, y+n))
    if x+n < 8:
        positions.append((x+n, y))
    if (x-n) >= 0:
        positions.append((x-n, y))
    if y-n >= 0:
        positions.append((x, y-n))
        if x+n < 8:
          positions.append((x+n, y-n))
        if x-n >=0:
          positions.append((x-n, y-n))
    return positions

# this is for chunks
# returns a dictionary of (x,y):hot_spot_value
def hotspot(chunks, board_dict):
  all_dict = {}
  for chunk in chunks:
    chunk_dict = {}
    for stack in chunk:
      poss_positions = possible_bomb_positions(stack[1], stack[2], 1)
      for position in poss_positions:
        if position not in chunk_dict and position not in token_positions(board_dict, "white"):
          chunk_dict[position] = 1
    #print(chunk_dict)
    for k in chunk_dict.keys():
      if k in all_dict:
        all_dict[k] += 1
      else:
        all_dict[k] = 1
  return all_dict