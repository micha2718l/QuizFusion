import os
import time

def detect_file_changes(file_path, interval=1):
    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            print("File has changed!")
            last_modified = current_modified
        time.sleep(interval)

# Usage
detect_file_changes("notebooks/kinematics.ipynb")