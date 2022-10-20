import qrcode


QR_IMG_NAME = "sampleQR_1.png"

QR_TEXT = """Questions:
Hair colour? Item carried?
2021-08-18; 16:37; S_Comm1; S02; 49.90440649280493; -98.27393447717382
"""


def create_qr(qr_text=QR_TEXT, qr_img_name=QR_IMG_NAME):
    """Creates QR code using QR_TEXT string

    Args:
        qr_text: (str) Text to encode in QR
        qr_img_name: (str) Image path name to save QR as

    Returns:
    """
    img = qrcode.make(qr_text)
    img.save(qr_img_name)


if __name__ == "__main__":
    create_qr()
