import os
import logging
from datetime import datetime
from utils import get_root_dir

DIRECTORY = get_root_dir()


def setup_logging(log_directory='') -> None:
    """Standardized logging system starter
    Call in every file for logging system to write to same file

    :param log_directory: (str) Custom log path
    :return: None
    """
    log_filename = f"log-{datetime.today().strftime('%Y-%m-%d-%H')}.log"
    if log_directory:
        if not os.path.isdir(log_directory):
            os.mkdir(log_directory)
        log_path = f"{log_directory}/{log_filename}"
    else:
        log_path = f"{DIRECTORY}/logs"
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        log_path += f"/{log_filename}"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(log_path, 'a', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
