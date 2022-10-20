from cv2 import cv2
import numpy as np
import time
from pyzbar.pyzbar import decode
import qr_format as qr_format

import logging
from logging_script import start_logging
start_logging()


class QRReader:

    def __init__(self):
        self.raw_message = None
        self.message = None

    def read(self, camera, active_display=False, display_time=15, image=None) \
            -> None:
        """Using input image, finds QR code within the image, and saves the
        decoded and formatted message

        Args:
            camera: OpenCV VideoCapture object
            active_display: (bool) Display the camera feed
            display_time: (int) How long to run the QR reader for
            image: optional (str) Path to image file

        Returns:

        """
        logging.info(f"Starting QR Reader at {time.time()}")
        qr_found = False
        end_time = time.time() + display_time
        while not qr_found or (active_display and time.time() < end_time):
            logging.info(f"Recapturing QR Image {time.time()}")
            if image:
                img = cv2.imread(image)
            else:
                success, img = camera.read()

            try:
                embedded_data = None
                # Decode(img) is an array of QRs; iterate to find embedded data
                for qr in decode(img):
                    # Converts embedded data to string format
                    embedded_data = qr.data.decode('utf-8')
                    logging.info(f"Decoded QR Data: \n {embedded_data}")

                    if active_display:
                        # Add border detection and overlay text
                        border = np.array([qr.polygon], np.int32)
                        border = border.reshape((-1, 1, 2))
                        border_text = qr.rect

                        cv2.polylines(img, [border], True, (255, 0, 255), 8)
                        cv2.putText(img, embedded_data,
                                    (border_text[0], border_text[1]),
                                    cv2.FONT_HERSHEY_PLAIN, 0.9,
                                    (255, 0, 255), 2)

                if embedded_data:
                    # Successful QR read
                    qr_found = True
                    if qr_format.check_msg_format(embedded_data):
                        self.raw_message = embedded_data
                        self.message = qr_format.msg_decoder(embedded_data)
                else:
                    if image:
                        break  # Image argument, attempt decoding QR once

                if active_display:
                    # Display QR found with overlaid border and text
                    cv2.imshow('QR Reader Image', img)
                    cv2.waitKey(1000)
            except Exception:
                # Error in Py zbar decoding, attempt again
                continue
