class PlayfairCipher:
    def __init__(self, key):
        self.key = self._prepare_key(key)
        self.matrix = self._create_matrix()

    def _prepare_key(self, key):
        key = ''.join(char.upper() for char in key if char.isalpha())
        key = key.replace("J", "I")

        result = ""
        for char in key:
            if char not in result:
                result += char

        return result

    def _create_matrix(self):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        combined = self.key + alphabet

        matrix_chars = ""
        for char in combined:
            if char not in matrix_chars:
                matrix_chars += char

        return [
            matrix_chars[i:i + 5]
            for i in range(0, 25, 5)
        ]

    def _find_position(self, char):
        for row in range(5):
            for col in range(5):
                if self.matrix[row][col] == char:
                    return row, col
        return None

    def _prepare_text(self, text):
        text = ''.join(char.upper() for char in text if char.isalpha())
        text = text.replace("J", "I")

        prepared = ""
        i = 0

        while i < len(text):
            first = text[i]

            if i + 1 < len(text):
                second = text[i + 1]

                if first == second:
                    prepared += first + "X"
                    i += 1
                else:
                    prepared += first + second
                    i += 2
            else:
                prepared += first + "X"
                i += 1

        return prepared

    def encrypt(self, plaintext):
        plaintext = self._prepare_text(plaintext)
        ciphertext = ""

        for i in range(0, len(plaintext), 2):
            first = plaintext[i]
            second = plaintext[i + 1]

            row1, col1 = self._find_position(first)
            row2, col2 = self._find_position(second)

            if row1 == row2:
                ciphertext += self.matrix[row1][(col1 + 1) % 5]
                ciphertext += self.matrix[row2][(col2 + 1) % 5]

            elif col1 == col2:
                ciphertext += self.matrix[(row1 + 1) % 5][col1]
                ciphertext += self.matrix[(row2 + 1) % 5][col2]

            else:
                ciphertext += self.matrix[row1][col2]
                ciphertext += self.matrix[row2][col1]

        return ciphertext

    def decrypt(self, ciphertext):
        ciphertext = ''.join(
            char.upper() for char in ciphertext if char.isalpha()
        )
        ciphertext = ciphertext.replace("J", "I")

        plaintext = ""

        for i in range(0, len(ciphertext), 2):
            first = ciphertext[i]
            second = ciphertext[i + 1]

            row1, col1 = self._find_position(first)
            row2, col2 = self._find_position(second)

            if row1 == row2:
                plaintext += self.matrix[row1][(col1 - 1) % 5]
                plaintext += self.matrix[row2][(col2 - 1) % 5]

            elif col1 == col2:
                plaintext += self.matrix[(row1 - 1) % 5][col1]
                plaintext += self.matrix[(row2 - 1) % 5][col2]

            else:
                plaintext += self.matrix[row1][col2]
                plaintext += self.matrix[row2][col1]

        return plaintext

    def display_matrix(self):
        for row in self.matrix:
            print(" ".join(row))