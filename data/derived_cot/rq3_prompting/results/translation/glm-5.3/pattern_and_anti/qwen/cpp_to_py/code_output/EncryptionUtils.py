class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def _isalpha(ch):
        return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')

    @staticmethod
    def _isupper(ch):
        return 'A' <= ch <= 'Z'

    @staticmethod
    def _c_mod(value, modulus=26):
        # C++ % truncates toward zero (result keeps sign of dividend),
        # unlike Python's floor-based %.
        result = abs(value) % modulus
        return result if value >= 0 else -result

    def caesar_cipher(self, plaintext, shift):
        ciphertext = []
        for ch in plaintext:
            if self._isalpha(ch):
                ascii_offset = 65 if self._isupper(ch) else 97
                shifted_char = chr(
                    self._c_mod(ord(ch.lower()) - ord('a') + shift) + ascii_offset
                )
                ciphertext.append(shifted_char)
            else:
                ciphertext.append(ch)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plain_text):
        encrypted_text = []
        key_index = 0
        key_length = len(self.key)
        for ch in plain_text:
            if self._isalpha(ch):
                shift = ord(self.key[key_index % key_length].lower()) - ord('a')
                encrypted_char = chr(
                    self._c_mod(ord(ch.lower()) - ord('a') + shift) + ord('a')
                )
                encrypted_text.append(
                    encrypted_char.upper() if self._isupper(ch) else encrypted_char
                )
                key_index += 1
            else:
                encrypted_text.append(ch)
        return ''.join(encrypted_text)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 0:
            raise ValueError("Rails must be greater than zero.")
        N = 101
        fence = [''] * N
        direction = -1
        row = 0

        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction

            fence[row] += ch
            row += direction

        encrypted_text = ''
        for i in range(rails):
            encrypted_text += fence[i]

        return encrypted_text