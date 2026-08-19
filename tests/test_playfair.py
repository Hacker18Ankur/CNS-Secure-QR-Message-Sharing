from src.crypto.playfair import PlayfairCipher


def main():
    key = "SECURITY"
    message = "HELLO WORLD"

    cipher = PlayfairCipher(key)

    print("\nPlayfair Matrix:")
    cipher.display_matrix()

    encrypted = cipher.encrypt(message)
    decrypted = cipher.decrypt(encrypted)

    print("\nOriginal Message :", message)
    print("Encrypted Message:", encrypted)
    print("Decrypted Message:", decrypted)


if __name__ == "__main__":
    main()