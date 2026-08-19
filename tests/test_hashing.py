from src.crypto.hashing import generate_hash, verify_hash


def main():
    original_message = "Meet me near the library"

    print("\nOriginal Message:")
    print(original_message)

    # Generate SHA-256 hash
    original_hash = generate_hash(original_message)

    print("\nSHA-256 Hash:")
    print(original_hash)

    # Verify unchanged message
    valid = verify_hash(original_message, original_hash)

    print("\nVerification of Original Message:")
    print("Valid" if valid else "Invalid")

    # Test modified message
    modified_message = "Meet me near the laboratory"

    modified_valid = verify_hash(modified_message, original_hash)

    print("\nVerification of Modified Message:")
    print("Valid" if modified_valid else "Tampering Detected")


if __name__ == "__main__":
    main()