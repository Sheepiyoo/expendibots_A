import test_case_generator
import subprocess
from shutil import move
import glob
import board_inspector

target = 10000

good_count = 0
bad_count = 0
test_count = 0

"""
# Check all cases within a folder
for filename in glob.glob(r"auto_test\2020-04-02\success_1\*.json"):
    try:
        subprocess.check_output(["python", "-m", "search", filename], timeout=25)
    except:
        print("Failed")
        move(filename, os.path.join("true_failures", filename))

    else:
        print("Success")
        #move("test.json", "auto_test\\success\\" + str(good_count) + ".json")
"""

while test_count < target:
    test_case_generator.run()
    is_possible = board_inspector.check_valid_board_from_file("test.json")

    if is_possible == False:
        print("Invalid Board")
        continue

    try:
        subprocess.check_output(["python", "-m", "search", "test.json"], timeout=25)
    except:
        print("Failed")
        move("test.json", "auto_test\\failures\\" + str(bad_count) + ".json")
        bad_count += 1

    else:
        print("Success")
        move("test.json", "auto_test\\success\\" + str(good_count) + ".json")
        good_count += 1

    test_count += 1

