import os

from src.crypto.playfair import PlayfairCipher
from src.crypto.hashing import generate_hash, verify_hash
from src.qr.qr_handler import create_secure_qr_data, generate_qr


def secure_message_workflow():
    print("\n======================================")
    print(" SECURE QR MESSAGE SHARING SYSTEM")
    print("======================================")

    # Step 1: Get message and key
    message = input("\nEnter your secret message: ")
    key = input("Enter encryption key: ")

    # Step 2: Playfair encryption
    cipher = PlayfairCipher(key)
    encrypted_message = cipher.encrypt(message)

    print("\n[1] Playfair Encryption")
    print("Encrypted Message:", encrypted_message)

    # Step 3: SHA-256 hash
    message_hash = generate_hash(encrypted_message)

    print("\n[2] SHA-256 Integrity Hash")
    print("Hash:", message_hash)

    # Step 4: Prepare QR data
    qr_data = create_secure_qr_data(
        encrypted_message,
        message_hash
    )

    # Step 5: Generate QR code
    filename = "secure_message_qr.png"

    generate_qr(
        qr_data,
        filename
    )

    print("\n[3] QR Code Generation")
    print("QR Code created:", os.path.abspath(filename))

    print("\n======================================")
    print("SECURE MESSAGE CREATED SUCCESSFULLY")
    print("======================================")

    return encrypted_message, message_hash, key


def verify_and_decrypt(encrypted_message, original_hash, key):
    print("\n======================================")
    print(" MESSAGE VERIFICATION")
    print("======================================")

    # Verify integrity
    is_valid = verify_hash(
        encrypted_message,
        original_hash
    )

    if not is_valid:
        print("\n⚠ WARNING: TAMPERING DETECTED!")
        print("The encrypted message has been modified.")
        return

    print("\n✓ SHA-256 verification successful.")
    print("✓ Message integrity confirmed.")

    # Decrypt message
    cipher = PlayfairCipher(key)
    decrypted_message = cipher.decrypt(encrypted_message)

    print("\nDecrypted Message:")
    print(decrypted_message)

    print("\n======================================")
    print("MESSAGE VERIFIED AND DECRYPTED")
    print("======================================")


if __name__ == "__main__":

    encrypted, message_hash, key = secure_message_workflow()

    verify_and_decrypt(
        encrypted,
        message_hash,
        key
    )