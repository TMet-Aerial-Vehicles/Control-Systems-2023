import cv2
from pyzbar.pyzbar import decode

from server.qr import AllQr


QR_LST = AllQr()


def test_qr3():
    # Read Image
    img_path = "qr_images/Updated_QR3.png"
    img = cv2.imread(img_path)

    # Read QR from Image
    embedded_data = ""
    for qr in decode(img):
        embedded_data = qr.data.decode('utf-8')

    # Process QR 3
    print(QR_LST.qrs[2].process(embedded_data))

    # Read QR 3 Data
    print(QR_LST.qrs[2].convert_to_dict())


if __name__ == "__main__":
    # Note: You may need to set server as root directory
    # In Pycharm, right clicks /server, Mark Directory as Sources Root
    test_qr3()
