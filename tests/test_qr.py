from src.qr.qr_handler import generate_qr


def main():
    test_data = "Hello! This is a secure message."

    filename = generate_qr(
        test_data,
        "test_qr.png"
    )

    print("QR code generated successfully!")
    print("File:", filename)


if __name__ == "__main__":
    main()