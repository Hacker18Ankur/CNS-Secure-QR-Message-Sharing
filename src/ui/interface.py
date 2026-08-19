import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from src.crypto.playfair import PlayfairCipher
from src.crypto.hashing import generate_hash, verify_hash
from src.qr.qr_handler import (
    create_secure_qr_data,
    generate_qr,
    decode_qr,
    read_secure_qr_data,
)


class SecureQRApp:
    def __init__(self, root):
        self.root = root

        self.root.title("Secure QR Message Sharing System")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        self.qr_filename = None
        self.qr_preview = None

        self.create_widgets()

    def create_widgets(self):
        # Main title
        title = ttk.Label(
            self.root,
            text="🔐 Secure QR Message Sharing System",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=20)

        subtitle = ttk.Label(
            self.root,
            text="Playfair Cipher • SHA-256 • QR Code",
            font=("Arial", 11)
        )

        subtitle.pack(pady=(0, 15))

        # Notebook
        notebook = ttk.Notebook(self.root)
        notebook.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # Sender tab
        sender_frame = ttk.Frame(notebook, padding=20)
        notebook.add(sender_frame, text="🔒 Send Message")

        self.create_sender_tab(sender_frame)

        # Receiver tab
        receiver_frame = ttk.Frame(notebook, padding=20)
        notebook.add(receiver_frame, text="🔓 Receive Message")

        self.create_receiver_tab(receiver_frame)

    # ---------------- SEND TAB ----------------

    def create_sender_tab(self, parent):

        ttk.Label(
            parent,
            text="Secret Message",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        self.message_text = tk.Text(
            parent,
            height=6,
            font=("Arial", 11)
        )

        self.message_text.pack(
            fill="x",
            pady=(5, 15)
        )

        ttk.Label(
            parent,
            text="Encryption Key",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        self.sender_key = ttk.Entry(
            parent,
            show="*"
        )

        self.sender_key.pack(
            fill="x",
            pady=(5, 15)
        )

        generate_button = ttk.Button(
            parent,
            text="🔒 Generate Secure QR",
            command=self.generate_secure_qr
        )

        generate_button.pack(pady=10)

        self.sender_status = ttk.Label(
            parent,
            text="Status: Ready",
            font=("Arial", 11)
        )

        self.sender_status.pack(pady=10)

        self.qr_label = ttk.Label(parent)
        self.qr_label.pack(pady=10)

    def generate_secure_qr(self):

        message = self.message_text.get(
            "1.0",
            tk.END
        ).strip()

        key = self.sender_key.get().strip()

        if not message:
            messagebox.showerror(
                "Error",
                "Please enter a secret message."
            )
            return

        if not key:
            messagebox.showerror(
                "Error",
                "Please enter an encryption key."
            )
            return

        try:

            # Playfair encryption
            cipher = PlayfairCipher(key)
            encrypted_message = cipher.encrypt(message)

            # SHA-256
            message_hash = generate_hash(
                encrypted_message
            )

            # QR data
            qr_data = create_secure_qr_data(
                encrypted_message,
                message_hash
            )

            # Generate QR
            self.qr_filename = "secure_message_qr.png"

            generate_qr(
                qr_data,
                self.qr_filename
            )

            # Display QR
            image = Image.open(
                self.qr_filename
            )

            image = image.resize(
                (250, 250)
            )

            self.qr_preview = ImageTk.PhotoImage(
                image
            )

            self.qr_label.config(
                image=self.qr_preview
            )

            self.sender_status.config(
                text="✓ Secure QR generated successfully."
            )

            messagebox.showinfo(
                "Success",
                "Secure QR code generated successfully!"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ---------------- RECEIVE TAB ----------------

    def create_receiver_tab(self, parent):

        ttk.Label(
            parent,
            text="QR Code Image",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        browse_button = ttk.Button(
            parent,
            text="📂 Select QR Image",
            command=self.select_qr
        )

        browse_button.pack(
            anchor="w",
            pady=10
        )

        self.selected_file_label = ttk.Label(
            parent,
            text="No QR image selected."
        )

        self.selected_file_label.pack(
            anchor="w",
            pady=5
        )

        ttk.Label(
            parent,
            text="Decryption Key",
            font=("Arial", 12, "bold")
        ).pack(
            anchor="w",
            pady=(15, 0)
        )

        self.receiver_key = ttk.Entry(
            parent,
            show="*"
        )

        self.receiver_key.pack(
            fill="x",
            pady=5
        )

        verify_button = ttk.Button(
            parent,
            text="🔓 Verify & Decrypt",
            command=self.verify_and_decrypt
        )

        verify_button.pack(pady=15)

        ttk.Label(
            parent,
            text="Status",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        self.receiver_status = ttk.Label(
            parent,
            text="Status: Waiting for QR image"
        )

        self.receiver_status.pack(
            anchor="w",
            pady=5
        )

        ttk.Label(
            parent,
            text="Decrypted Message",
            font=("Arial", 12, "bold")
        ).pack(
            anchor="w",
            pady=(15, 0)
        )

        self.decrypted_text = tk.Text(
            parent,
            height=7,
            font=("Arial", 11)
        )

        self.decrypted_text.pack(
            fill="both",
            expand=True,
            pady=5
        )

    def select_qr(self):

        filename = filedialog.askopenfilename(
            title="Select QR Code",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPG files", "*.jpg"),
                ("JPEG files", "*.jpeg"),
                ("All files", "*.*")
            ]
        )

        if filename:

            self.qr_filename = filename

            self.selected_file_label.config(
                text=os.path.basename(filename)
            )

            self.receiver_status.config(
                text="QR image selected. Enter key and verify."
            )

    def verify_and_decrypt(self):

        if not self.qr_filename:

            messagebox.showerror(
                "Error",
                "Please select a QR image first."
            )

            return

        key = self.receiver_key.get().strip()

        if not key:

            messagebox.showerror(
                "Error",
                "Please enter the decryption key."
            )

            return

        try:

            # Decode QR
            qr_data = decode_qr(
                self.qr_filename
            )

            # Read QR information
            data = read_secure_qr_data(
                qr_data
            )

            encrypted_message = data[
                "encrypted_message"
            ]

            original_hash = data[
                "hash"
            ]

            # Verify SHA-256
            is_valid = verify_hash(
                encrypted_message,
                original_hash
            )

            if not is_valid:

                self.receiver_status.config(
                    text="⚠ TAMPERING DETECTED!"
                )

                self.decrypted_text.delete(
                    "1.0",
                    tk.END
                )

                messagebox.showerror(
                    "Security Warning",
                    "Message integrity verification failed."
                )

                return

            # Decrypt
            cipher = PlayfairCipher(key)

            decrypted_message = cipher.decrypt(
                encrypted_message
            )

            self.decrypted_text.delete(
                "1.0",
                tk.END
            )

            self.decrypted_text.insert(
                tk.END,
                decrypted_message
            )

            self.receiver_status.config(
                text="✓ Integrity verified. Message decrypted."
            )

            messagebox.showinfo(
                "Success",
                "Message verified and decrypted successfully!"
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )


def launch_app():

    root = tk.Tk()

    app = SecureQRApp(root)

    root.mainloop()