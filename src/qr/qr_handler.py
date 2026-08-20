import json
import qrcode
import cv2


def generate_qr(data, filename="secure_message_qr.png"):
    """
    Generate a QR code from the supplied data.
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


def create_secure_qr_data(
    encrypted_message,
    message_hash,
    key_hash
):
    """
    Create the data that will be stored inside the QR code.

    The QR stores:
    1. Playfair encrypted message
    2. SHA-256 hash of encrypted message
    3. SHA-256 hash of encryption key

    The actual encryption key is NEVER stored.
    """

    data = {
        "algorithm": "Playfair Cipher",
        "hash_algorithm": "SHA-256",
        "encrypted_message": encrypted_message,
        "message_hash": message_hash,
        "key_hash": key_hash
    }

    return json.dumps(data)


def read_secure_qr_data(data):
    """
    Convert QR JSON data into a Python dictionary.
    """

    return json.loads(data)


def decode_qr(filename):
    """
    Decode a QR code from an image file.
    """

    detector = cv2.QRCodeDetector()

    image = cv2.imread(filename)

    if image is None:
        raise FileNotFoundError(
            f"QR image not found: {filename}"
        )

    data, points, _ = detector.detectAndDecode(
        image
    )

    if not data:
        raise ValueError(
            "Could not decode the QR code."
        )

    return data