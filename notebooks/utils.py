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
    while os.getcwd().split("\\")[-1] != "fil-rouge-pollinisateurs":
        os.chdir("..")
        if os.getcwd() == "\\":
            print("Error: Could not find parent directory")
            sys.exit()
    sys.path.append(os.getcwd())
    print("Current working directory: ", os.getcwd())
