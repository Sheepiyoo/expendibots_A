import argparse
import glob
import json
from search.util import print_board
import search.game as game
import search.big_brains as ai
import hotspot
import os
from shutil import move

def check_valid_board(data):
    white_available = ai.count_tokens(data["white"])
    white_needed = 0

    if(len(data["black"]) == 0): return False
    
    #Remove white tokens
    data = {"black": data["black"]}

    #Remove stacks until none remaining
    while(len(data["black"]) > 0):
        chunks = ai.get_chunks(data)
        result = hotspot.hotspot(chunks, data)
        
        #Convert to string representation
        string_result = {}
        for key in result.keys():
            string_result[key] = str(result[key])

        #print_board(game.get_grid_format(data))
        
        #Unionise dictionaries
        full_data = game.get_grid_format(data)
        full_data.update(result)
        #print(full_data)
        #print_board(full_data)

        x, y = max(string_result, key=string_result.get)
        temp_stack = [1, x, y]
        data["black"].append(temp_stack)
        data = game.boom(temp_stack, data)


        #print_board(game.get_grid_format(data))

        white_needed += 1
        #print(white_needed)
    
    return white_available >= white_needed

def check_valid_board_from_file(filename):
    with open(filename) as file:
        data = json.load(file)

    is_possible = check_valid_board(data)

    return is_possible

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect board configurations.")
    parser.add_argument('--folder', type=str, required=True, help='Folder of test cases')
    args = parser.parse_args()

    for filename in glob.glob(args.folder + '\*.json'):
        with open(filename) as file:
            data = json.load(file)

        is_possible = check_valid_board(data)

        print(filename, is_possible)
        
        if is_possible == False:
           os.remove(filename)
        
