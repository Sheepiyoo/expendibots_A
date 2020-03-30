import test_case_generator
import subprocess
from shutil import move

good_count = 0
bad_count = 0

while True:
    test_case_generator.run()
    try:
        p = subprocess.run(["python", "-m", "search", "test.json"], timeout=30)
    except:
        print("Failed")
        move("test.json", "auto_test\\failures\\" + str(bad_count) + ".json")
        bad_count += 1

    else:
        print("Success")
        move("test.json", "auto_test\\success\\" + str(good_count) + ".json")
        good_count += 1

