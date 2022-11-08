# Imports

import logging
from logging_script import start_logging
from qr.qr_reader import QRReader

start_logging()

if __name__ == "__main__":
    logging.info("Initiating Task 2")
    qr = QRReader()
    qr.read(image="./qr/images/task2qr.png")
