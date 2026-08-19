from src.crypto.hashing import generate_hash, verify_hash


def main():

    original_message = "SECRET MESSAGE"

    print("======================================")
    print("       SHA-256 TAMPERING TEST")
    print("======================================")

    # Original hash
    original_hash = generate_hash(original_message)

    print("\nOriginal Message:")
    print(original_message)

    print("\nOriginal SHA-256:")
    print(original_hash)

    # Verify original
    print("\nTesting original message...")

    if verify_hash(original_message, original_hash):
        print("✓ Integrity verified")
    else:
        print("✗ Verification failed")

    # Modify message
    modified_message = "SECRET MESSSAGE"

    print("\nModified Message:")
    print(modified_message)

    # Verify modified message using original hash
    print("\nTesting modified message...")

    if verify_hash(modified_message, original_hash):
        print("✗ Security test failed")
    else:
        print("⚠ TAMPERING DETECTED")

    print("\n======================================")
    print("         SECURITY TEST COMPLETE")
    print("======================================")


if __name__ == "__main__":
    main()