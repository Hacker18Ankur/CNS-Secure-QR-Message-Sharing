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