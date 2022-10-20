# Defines specified competition QR format

def check_msg_format(msg: str) -> bool:
    # TODO: Update to 2023 competition format
    """Check if decoded QR message matches competition format

    Args:
        msg: (str) of decoded message to check format

    Returns: (bool) of correct formatting
    """
    msg_new = msg.splitlines()
    if len(msg_new) != 3:
        return False
    if "Questions:" not in msg_new[0]:
        return False

    qr_line_3 = msg_new[2].split(';')
    if len(qr_line_3) != 5:
        return False
    try:
        # Check longitude, latitude
        float(qr_line_3[4])
        float(qr_line_3[5])
    except ValueError:
        return False

    return True


def msg_decoder(msg):
    # TODO: Update to 2023 competition format
    """Formulate the QR code into a digestible dictionary

    Format:
    Questions:\n
    Word word? Word word? Word word?\n
    Date; Time; device_id; sensor_id; longitude; latitude

    Example Format
    Questions:
    Tshirt colour? Hair colour? Item carried?
    2021-08-18; 16:37; S_Comm1; S02; 49.90440649280493; -98.27393447717382

    """
    msg_new = msg.splitlines()
    response = {
        'questions': msg_new[1].split('?')
    }

    msg_data = msg_new[2].split(';')
    response['date'] = msg_data[0].strip()
    response['time'] = msg_data[1].strip()
    response['device_id'] = msg_data[2].strip()
    response['sensor_id'] = msg_data[3].strip()

    response['longitude'] = float(msg_data[4].strip())
    response['latitude'] = float(msg_data[5].strip())

    return response

