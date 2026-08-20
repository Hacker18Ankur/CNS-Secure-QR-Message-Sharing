import hashlib


def generate_hash(message):
    """
    Generate a SHA-256 hash for the given message.
    """

    return hashlib.sha256(
        message.encode("utf-8")
    ).hexdigest()


def verify_hash(message, original_hash):
    """
    Verify whether the message matches
    the original SHA-256 hash.
    """

    current_hash = generate_hash(
        message
    )

    return current_hash == original_hash


def generate_key_hash(key):
    """
    Generate SHA-256 hash of the encryption key.

    The actual key is never stored.
    Only its hash is stored in the QR code.
    """

    return hashlib.sha256(
        key.encode("utf-8")
    ).hexdigest()