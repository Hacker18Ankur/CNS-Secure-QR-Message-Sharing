from src.qr.qr_handler import (
    generate_qr,
    decode_qr,
)


def main():
    test_data = "Hello! This is a secure message."

    filename = "test_qr.png"

    # Generate QR
    generate_qr(test_data, filename)

    print("QR code generated successfully!")
    print("File:", filename)

    # Decode QR
    decoded_data = decode_qr(filename)

    print("\nDecoded QR Data:")
    print(decoded_data)

    # Verify
    if decoded_data == test_data:
        print("\nQR generation and decoding successful!")
    else:
        print("\nQR verification failed!")


if __name__ == "__main__":
    main()