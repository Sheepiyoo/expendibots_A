import argparse
import glob
import json
from search.util import print_board
from search.game import get_grid_format
import os

parser = argparse.ArgumentParser(description="Inspect board configurations.")
parser.add_argument('--folder', type=str, required=True, help='Folder of test cases')
args = parser.parse_args()

for filename in glob.glob(args.folder + '\*.json'):
    with open(filename) as file:
        data = json.load(file)

    print_board(get_grid_format(data))
    is_possible = input("Press N to delete\n")

    if is_possible == 'N':
        os.remove(filename)
    


