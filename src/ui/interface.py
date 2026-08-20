import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.crypto.playfair import PlayfairCipher
from src.crypto.hashing import (
    generate_hash,
    verify_hash,
    generate_key_hash
)

from src.qr.qr_handler import (
    create_secure_qr_data,
    generate_qr,
    decode_qr,
    read_secure_qr_data
)


class SecureQRApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Secure QR Message Sharing System"
        )

        self.root.geometry(
            "900x700"
        )

        self.root.minsize(
            800,
            600
        )

        # ----------------------------------
        # VARIABLES
        # ----------------------------------

        self.qr_filename = None

        self.sender_message = tk.StringVar()
        self.sender_key = tk.StringVar()

        self.receiver_key = tk.StringVar()

        self.qr_path_var = tk.StringVar(
            value="No QR image selected"
        )

        # ----------------------------------
        # MAIN STYLE
        # ----------------------------------

        self.setup_style()

        # ----------------------------------
        # BUILD GUI
        # ----------------------------------

        self.create_header()
        self.create_notebook()

        self.create_sender_tab()
        self.create_receiver_tab()

    # ======================================
    # STYLE
    # ======================================

    def setup_style(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 22, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11)
        )

        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 13, "bold")
        )

        style.configure(
            "Normal.TLabel",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

    # ======================================
    # HEADER
    # ======================================

    def create_header(self):

        header = ttk.Frame(
            self.root,
            padding=(20, 18)
        )

        header.pack(
            fill="x"
        )

        title = ttk.Label(
            header,
            text="🔐 Secure QR Message Sharing System",
            style="Title.TLabel"
        )

        title.pack()

        subtitle = ttk.Label(
            header,
            text="Playfair Cipher • SHA-256 • QR Code",
            style="Subtitle.TLabel"
        )

        subtitle.pack(
            pady=(5, 0)
        )

    # ======================================
    # NOTEBOOK
    # ======================================

    def create_notebook(self):

        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.sender_tab = ttk.Frame(
            self.notebook,
            padding=20
        )

        self.receiver_tab = ttk.Frame(
            self.notebook,
            padding=20
        )

        self.notebook.add(
            self.sender_tab,
            text="🔒 Send Message"
        )

        self.notebook.add(
            self.receiver_tab,
            text="📥 Receive Message"
        )

    # ======================================
    # SENDER TAB
    # ======================================

    def create_sender_tab(self):

        # ----------------------------------
        # SECRET MESSAGE
        # ----------------------------------

        ttk.Label(
            self.sender_tab,
            text="Secret Message",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        self.message_text = tk.Text(
            self.sender_tab,
            height=8,
            wrap="word",
            font=("Segoe UI", 11)
        )

        self.message_text.pack(
            fill="x",
            pady=(0, 20)
        )

        # ----------------------------------
        # ENCRYPTION KEY
        # ----------------------------------

        ttk.Label(
            self.sender_tab,
            text="Encryption Key",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        self.sender_key_entry = ttk.Entry(
            self.sender_tab,
            textvariable=self.sender_key,
            show="*",
            font=("Segoe UI", 11)
        )

        self.sender_key_entry.pack(
            fill="x",
            pady=(0, 5)
        )

        ttk.Label(
            self.sender_tab,
            text=(
                "The key is used for Playfair encryption "
                "and is not stored directly in the QR code."
            ),
            style="Normal.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        # ----------------------------------
        # GENERATE BUTTON
        # ----------------------------------

        generate_button = ttk.Button(
            self.sender_tab,
            text="🔐 Generate Secure QR",
            style="Action.TButton",
            command=self.generate_secure_qr
        )

        generate_button.pack(
            pady=10
        )

        # ----------------------------------
        # STATUS
        # ----------------------------------

        ttk.Label(
            self.sender_tab,
            text="Status",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.sender_status = ttk.Label(
            self.sender_tab,
            text="Ready to create a secure message.",
            style="Normal.TLabel"
        )

        self.sender_status.pack(
            anchor="w"
        )

        # ----------------------------------
        # ENCRYPTED MESSAGE
        # ----------------------------------

        ttk.Label(
            self.sender_tab,
            text="Encrypted Message",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.encrypted_text = tk.Text(
            self.sender_tab,
            height=5,
            wrap="word",
            font=("Consolas", 10)
        )

        self.encrypted_text.pack(
            fill="x"
        )

    # ======================================
    # RECEIVER TAB
    # ======================================

    def create_receiver_tab(self):

        # ----------------------------------
        # QR IMAGE
        # ----------------------------------

        ttk.Label(
            self.receiver_tab,
            text="QR Code Image",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        qr_frame = ttk.Frame(
            self.receiver_tab
        )

        qr_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        select_button = ttk.Button(
            qr_frame,
            text="📁 Select QR Image",
            command=self.select_qr_image
        )

        select_button.pack(
            side="left"
        )

        ttk.Label(
            qr_frame,
            textvariable=self.qr_path_var,
            style="Normal.TLabel"
        ).pack(
            side="left",
            padx=15
        )

        # ----------------------------------
        # DECRYPTION KEY
        # ----------------------------------

        ttk.Label(
            self.receiver_tab,
            text="Decryption Key",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=(15, 8)
        )

        self.receiver_key_entry = ttk.Entry(
            self.receiver_tab,
            textvariable=self.receiver_key,
            show="*",
            font=("Segoe UI", 11)
        )

        self.receiver_key_entry.pack(
            fill="x",
            pady=(0, 20)
        )

        # ----------------------------------
        # VERIFY BUTTON
        # ----------------------------------

        verify_button = ttk.Button(
            self.receiver_tab,
            text="🔓 Verify & Decrypt",
            style="Action.TButton",
            command=self.verify_and_decrypt
        )

        verify_button.pack(
            pady=10
        )

        # ----------------------------------
        # STATUS
        # ----------------------------------

        ttk.Label(
            self.receiver_tab,
            text="Status",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.receiver_status = ttk.Label(
            self.receiver_tab,
            text="Select a QR image and enter the decryption key.",
            style="Normal.TLabel"
        )

        self.receiver_status.pack(
            anchor="w"
        )

        # ----------------------------------
        # DECRYPTED MESSAGE
        # ----------------------------------

        ttk.Label(
            self.receiver_tab,
            text="Decrypted Message",
            style="Section.TLabel"
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.decrypted_text = tk.Text(
            self.receiver_tab,
            height=8,
            wrap="word",
            font=("Segoe UI", 11)
        )

        self.decrypted_text.pack(
            fill="both",
            expand=True
        )

    # ======================================
    # GENERATE SECURE QR
    # ======================================

    def generate_secure_qr(self):

        message = self.message_text.get(
            "1.0",
            tk.END
        ).strip()

        key = self.sender_key.get().strip()

        # ----------------------------------
        # INPUT VALIDATION
        # ----------------------------------

        if not message:

            messagebox.showerror(
                "Missing Message",
                "Please enter a secret message."
            )

            return

        if not key:

            messagebox.showerror(
                "Missing Key",
                "Please enter an encryption key."
            )

            return

        try:

            # ----------------------------------
            # PLAYFAIR ENCRYPTION
            # ----------------------------------

            cipher = PlayfairCipher(
                key
            )

            encrypted_message = cipher.encrypt(
                message
            )

            # ----------------------------------
            # SHA-256 MESSAGE HASH
            # ----------------------------------

            message_hash = generate_hash(
                encrypted_message
            )

            # ----------------------------------
            # SHA-256 KEY HASH
            # ----------------------------------

            key_hash = generate_key_hash(
                key
            )

            # ----------------------------------
            # CREATE QR DATA
            # ----------------------------------

            qr_data = create_secure_qr_data(
                encrypted_message,
                message_hash,
                key_hash
            )

            # ----------------------------------
            # QR FILE
            # ----------------------------------

            filename = os.path.join(
                os.getcwd(),
                "secure_message_qr.png"
            )

            generate_qr(
                qr_data,
                filename
            )

            self.qr_filename = filename

            # ----------------------------------
            # DISPLAY ENCRYPTED MESSAGE
            # ----------------------------------

            self.encrypted_text.delete(
                "1.0",
                tk.END
            )

            self.encrypted_text.insert(
                tk.END,
                encrypted_message
            )

            # ----------------------------------
            # STATUS
            # ----------------------------------

            self.sender_status.config(
                text=(
                    "✓ Secure QR created successfully: "
                    + filename
                )
            )

            messagebox.showinfo(
                "Success",
                "Secure QR code created successfully!\n\n"
                "Algorithms used:\n"
                "✓ Playfair Cipher\n"
                "✓ SHA-256\n"
                "✓ QR Code"
            )

        except Exception as error:

            self.sender_status.config(
                text="❌ Error while creating QR code."
            )

            messagebox.showerror(
                "Encryption Error",
                str(error)
            )

    # ======================================
    # SELECT QR IMAGE
    # ======================================

    def select_qr_image(self):

        filename = filedialog.askopenfilename(
            title="Select Secure QR Image",
            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg *.bmp"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not filename:

            return

        self.qr_filename = filename

        self.qr_path_var.set(
            filename
        )

        self.receiver_status.config(
            text="✓ QR image selected. Enter the decryption key."
        )

    # ======================================
    # VERIFY AND DECRYPT
    # ======================================

    def verify_and_decrypt(self):

        # ----------------------------------
        # CHECK QR IMAGE
        # ----------------------------------

        if not self.qr_filename:

            messagebox.showerror(
                "Missing QR Image",
                "Please select a QR image first."
            )

            return

        # ----------------------------------
        # GET KEY
        # ----------------------------------

        key = self.receiver_key.get().strip()

        if not key:

            messagebox.showerror(
                "Missing Key",
                "Please enter the decryption key."
            )

            return

        try:

            # ----------------------------------
            # STEP 1: DECODE QR
            # ----------------------------------

            qr_data = decode_qr(
                self.qr_filename
            )

            # ----------------------------------
            # STEP 2: READ QR DATA
            # ----------------------------------

            data = read_secure_qr_data(
                qr_data
            )

            encrypted_message = data[
                "encrypted_message"
            ]

            original_hash = data[
                "message_hash"
            ]

            stored_key_hash = data[
                "key_hash"
            ]

            # ----------------------------------
            # STEP 3: VERIFY DECRYPTION KEY
            # ----------------------------------

            entered_key_hash = generate_key_hash(
                key
            )

            if entered_key_hash != stored_key_hash:

                self.receiver_status.config(
                    text="❌ Invalid decryption key."
                )

                self.decrypted_text.delete(
                    "1.0",
                    tk.END
                )

                messagebox.showerror(
                    "Invalid Key",
                    "❌ Wrong decryption key!\n\n"
                    "The message cannot be decrypted."
                )

                return

            # ----------------------------------
            # CORRECT KEY
            # ----------------------------------

            self.receiver_status.config(
                text=(
                    "✓ Correct key. "
                    "Checking message integrity..."
                )
            )

            # ----------------------------------
            # STEP 4: VERIFY SHA-256
            # ----------------------------------

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
                    "⚠ TAMPERING DETECTED!\n\n"
                    "The encrypted message has been modified."
                )

                return

            # ----------------------------------
            # STEP 5: PLAYFAIR DECRYPTION
            # ----------------------------------

            cipher = PlayfairCipher(
                key
            )

            decrypted_message = cipher.decrypt(
                encrypted_message
            )

            # ----------------------------------
            # DISPLAY MESSAGE
            # ----------------------------------

            self.decrypted_text.delete(
                "1.0",
                tk.END
            )

            self.decrypted_text.insert(
                tk.END,
                decrypted_message
            )

            # ----------------------------------
            # SUCCESS STATUS
            # ----------------------------------

            self.receiver_status.config(
                text=(
                    "✓ Integrity verified. "
                    "Message decrypted successfully."
                )
            )

            messagebox.showinfo(
                "Success",
                "✓ Correct decryption key!\n\n"
                "✓ SHA-256 integrity verified!\n\n"
                "✓ Message decrypted successfully!"
            )

        except KeyError:

            self.receiver_status.config(
                text="❌ Invalid QR data."
            )

            self.decrypted_text.delete(
                "1.0",
                tk.END
            )

            messagebox.showerror(
                "Invalid QR",
                "The selected QR code does not contain "
                "valid Secure QR Message data."
            )

        except ValueError as error:

            self.receiver_status.config(
                text="❌ Unable to decode QR code."
            )

            messagebox.showerror(
                "QR Error",
                str(error)
            )

        except Exception as error:

            self.receiver_status.config(
                text="❌ An unexpected error occurred."
            )

            messagebox.showerror(
                "Error",
                str(error)
            )


# ==========================================
# LAUNCH APPLICATION
# ==========================================

def launch_app():

    root = tk.Tk()

    app = SecureQRApp(
        root
    )

    root.mainloop()


# ==========================================
# DIRECT EXECUTION
# ==========================================

if __name__ == "__main__":

    launch_app()