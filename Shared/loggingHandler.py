import os
import logging
from datetime import datetime
from Shared.shared_utils import get_root_dir

# DIRECTORY = get_root_dir()


def setup_logging(log_directory="") -> None:
    """Standardized logging system starter
    Call in every file for logging system to write to same file

    :param log_directory: (str) Custom log directory
    :return: None
    """
    # Get/Create logging directory path
    root_path = get_root_dir()
    log_path = f"{root_path}/logs"
    log_path += f"/{log_directory}" if log_directory else ""
    if not os.path.isdir(log_path):
        os.mkdir(log_path)

    # Setup log filename path
    log_filename = f"log-{datetime.today().strftime('%Y-%m-%d-%H')}.log"
    log_path += f"/{log_filename}"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(log_path, 'a', 'utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
