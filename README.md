# 🔐 Secure QR-Based Secret Message Sharing System

A simple and secure message-sharing application that combines **Playfair Cipher, SHA-256 hashing, and QR Codes** to provide encrypted, integrity-verified communication.

## 📌 Project Overview

The Secure QR-Based Secret Message Sharing System allows a user to enter a secret message and protect it using a user-defined encryption key.

The system encrypts the message using the **Playfair Cipher**, generates a **SHA-256 hash** to verify message integrity, and stores the secured information inside a **QR Code**.

The receiver can scan/select the QR code and enter the correct decryption key to verify and decrypt the original message.

The system also detects incorrect decryption keys and message tampering.

## 🎯 Objectives

- Secure a secret message using encryption.
- Verify message integrity using SHA-256.
- Share encrypted information through a QR code.
- Prevent unauthorized decryption using key verification.
- Demonstrate the practical application of cryptographic algorithms.

## 🔐 Algorithms and Technologies Used

### 1. Playfair Cipher

Used for:

- Message encryption
- Message decryption
- Key-based transformation of the plaintext

### 2. SHA-256

Used for:

- Message integrity verification
- Detecting message tampering
- Secure verification of the decryption key

### 3. QR Code

Used for:

- Storing encrypted message information
- Sharing the secured message between sender and receiver

## ⚙️ System Workflow

```text
                SENDER
                   │
                   ▼
           Enter Secret Message
                   │
                   ▼
            Enter Encryption Key
                   │
                   ▼
          Playfair Cipher Encryption
                   │
                   ▼
          Generate SHA-256 Hash
                   │
                   ▼
          Generate Key Hash
                   │
                   ▼
              Generate QR
                   │
                   ▼
             QR Code Shared
                   │
                   ▼
               RECEIVER
                   │
                   ▼
            Select QR Image
                   │
                   ▼
           Enter Decryption Key
                   │
                   ▼
          Verify Key Hash
             /          \
          Wrong          Correct
            │               │
            ▼               ▼
       ❌ Reject       Verify SHA-256
                            │
                            ▼
                    Playfair Decryption
                            │
                            ▼
                     Original Message