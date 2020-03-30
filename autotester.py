import test_case_generator
import subprocess
from shutil import move

target = 1000

good_count = 0
bad_count = 0
test_count = 0

while test_count < target:
    test_case_generator.run()
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

