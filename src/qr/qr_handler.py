import json
import qrcode


def generate_qr(data, filename="secret_message.png"):
    """
    Generate a QR code from the provided data.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image()
    image.save(filename)

    return filename


def create_secure_qr_data(encrypted_message, message_hash):
    """
    Create structured data that will be stored inside the QR code.
    """
    data = {
        "algorithm": "Playfair Cipher",
        "hash_algorithm": "SHA-256",
        "encrypted_message": encrypted_message,
        "hash": message_hash
    }

    return json.dumps(data)


def read_secure_qr_data(data):
    """
    Convert QR data back into a Python dictionary.
    """
    return json.loads(data)