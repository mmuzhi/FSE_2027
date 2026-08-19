class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def _is_alpha(ch):
        # std::isalpha in the "C" locale: ASCII letters only
        return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'

    @staticmethod
    def _is_upper(ch):
        return 'A' <= ch <= 'Z'

    @staticmethod
    def _to_lower(ch):
        return chr(ord(ch) + 32) if 'A' <= ch <= 'Z' else ch

    @staticmethod
    def _to_upper(ch):
        return chr(ord(ch) - 32) if 'a' <= ch <= 'z' else ch

    @staticmethod
    def _mod(a):
        # C++ '%' truncates toward zero (may be negative); Python's floors.
        r = abs(a) % 26
        return r if a >= 0 else -r

    def caesar_cipher(self, plaintext, shift):
        ciphertext = []
        for ch in plaintext:
            if self._is_alpha(ch):
                ascii_offset = 65 if self._is_upper(ch) else 97
                shifted_char = chr(self._mod(ord(self._to_lower(ch)) - ord('a') + shift) + ascii_offset)
                ciphertext.append(shifted_char)
            else:
                ciphertext.append(ch)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plain_text):
        encrypted_text = []
        key_index = 0
        for ch in plain_text:
            if self._is_alpha(ch):
                shift = ord(self._to_lower(self.key[key_index % len(self.key)])) - ord('a')
                encrypted_char = chr(self._mod(ord(self._to_lower(ch)) - ord('a') + shift) + ord('a'))
                encrypted_text.append(self._to_upper(encrypted_char) if self._is_upper(ch) else encrypted_char)
                key_index += 1
            else:
                encrypted_text.append(ch)
        return ''.join(encrypted_text)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 0:
            raise ValueError("Rails must be greater than zero.")
        # Mirrors the fixed std::string fence[101] array (including the
        # rails == 1 quirk where rows run past `rails` but stay inside 101).
        fence = [''] * 101
        direction = -1
        row = 0

        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction

            fence[row] += ch
            row += direction

        return ''.join(fence[i] for i in range(rails))