import os
import sys

def setup_env_path() -> None:
    """
    Add parent directory to working directory
    It permits :
        - loading data from parent directory
        - loading modules from parent directory
    """
    print("Former working directory: ", os.getcwd())
    target_dir = "fil-rouge-pollinisateurs"
    while not os.getcwd().endswith(target_dir):
        os.chdir(os.path.pardir)
        if os.path.abspath(os.getcwd()) == os.path.abspath(os.path.join(os.getcwd(), os.pardir)):
            print("Error: Could not find parent directory")
            sys.exit()
    sys.path.append(os.getcwd())
    print("Current working directory: ", os.getcwd())