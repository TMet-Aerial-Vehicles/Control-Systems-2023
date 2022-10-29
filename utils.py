import os

PROJECT_NAME = "Control-Systems-2023"


def get_root_dir() -> str:
    """Returns a path to the project root directory, checking max 3 parents

    Returns: (str) Path to project root folder
    """
    cwd = os.getcwd()

    max_iterations = 3
    iter_count = 0
    while iter_count < max_iterations:
        if cwd.endswith(PROJECT_NAME):
            return cwd
        else:
            cwd = os.path.dirname(cwd)
    return os.getcwd()
