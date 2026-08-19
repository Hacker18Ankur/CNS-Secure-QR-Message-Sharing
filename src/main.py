import os

from src.crypto.playfair import PlayfairCipher
from src.crypto.hashing import generate_hash, verify_hash
from src.qr.qr_handler import (
    create_secure_qr_data,
    generate_qr,
    decode_qr,
    read_secure_qr_data,
)


def create_secure_message():
    print("\n======================================")
    print("        CREATE SECURE MESSAGE")
    print("======================================")

    message = input("\nEnter your secret message: ")
    key = input("Enter encryption key: ")

    if not message.strip():
        print("\nError: Message cannot be empty.")
        return

    if not key.strip():
        print("\nError: Encryption key cannot be empty.")
        return

    # Encrypt message
    cipher = PlayfairCipher(key)
    encrypted_message = cipher.encrypt(message)

    print("\n[1] Playfair Encryption")
    print("Encrypted Message:", encrypted_message)

    # Generate hash
    message_hash = generate_hash(encrypted_message)

    print("\n[2] SHA-256 Integrity Hash")
    print("Hash:", message_hash)

    # Create QR data
    qr_data = create_secure_qr_data(
        encrypted_message,
        message_hash
    )

    # Generate QR
    filename = "secure_message_qr.png"

    generate_qr(qr_data, filename)

    print("\n[3] QR Code Generation")
    print("QR Code created:")
    print(os.path.abspath(filename))

    print("\n======================================")
    print("SECURE MESSAGE CREATED SUCCESSFULLY")
    print("======================================")


def receive_secure_message():
    print("\n======================================")
    print("        RECEIVE SECURE MESSAGE")
    print("======================================")

    filename = input("\nEnter QR image filename: ")
    key = input("Enter decryption key: ")

    if not os.path.exists(filename):
        print("\nError: QR image file not found.")
        return

    if not key.strip():
        print("\nError: Decryption key cannot be empty.")
        return

    try:
        # Decode QR
        qr_data = decode_qr(filename)

        print("\n[1] QR Code Decoded")
        print("QR data received successfully.")

        # Read structured data
        data = read_secure_qr_data(qr_data)

        encrypted_message = data["encrypted_message"]
        original_hash = data["hash"]

        print("\n[2] Extracted Protected Data")
        print("Encrypted Message:", encrypted_message)
        print("Stored SHA-256:", original_hash)

        # Verify integrity
        is_valid = verify_hash(
            encrypted_message,
            original_hash
        )

        if not is_valid:
            print("\n======================================")
            print("⚠ TAMPERING DETECTED")
            print("======================================")
            print("The QR data has been modified.")
            return

        print("\n[3] SHA-256 Verification")
        print("✓ Integrity verification successful.")

        # Decrypt
        cipher = PlayfairCipher(key)
        decrypted_message = cipher.decrypt(encrypted_message)

        print("\n[4] Playfair Decryption")
        print("Decrypted Message:")
        print(decrypted_message)

        print("\n======================================")
        print("MESSAGE VERIFIED SUCCESSFULLY")
        print("======================================")

    except Exception as error:
        print("\nError:", error)


def main():
    while True:
        print("\n\n======================================")
        print("  SECURE QR MESSAGE SHARING SYSTEM")
        print("======================================")
        print("1. Create Secure Message")
        print("2. Receive Secure Message")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_secure_message()

        elif choice == "2":
            receive_secure_message()

        elif choice == "3":
            print("\nThank you for using the system.")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()