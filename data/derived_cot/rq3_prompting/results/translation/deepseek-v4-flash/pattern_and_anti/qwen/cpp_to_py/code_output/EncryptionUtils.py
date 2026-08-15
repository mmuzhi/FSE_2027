class EncryptionUtils:
    def __init__(self, key: str):
        self.key = key

    @staticmethod
    def _is_alpha(ch: str) -> bool:
        return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')

    @staticmethod
    def _is_upper(ch: str) -> bool:
        return 'A' <= ch <= 'Z'

    @staticmethod
    def _to_lower(ch: str) -> str:
        if 'A' <= ch <= 'Z':
            return chr(ord(ch) + 32)
        return ch

    @staticmethod
    def _to_upper(ch: str) -> str:
        if 'a' <= ch <= 'z':
            return chr(ord(ch) - 32)
        return ch

    @staticmethod
    def _cpp_mod(a: int, b: int) -> int:
        r = a % b
        if a < 0 and r != 0:
            r -= b
        return r

    def caesar_cipher(self, plaintext: str, shift: int) -> str:
        ciphertext = []
        for ch in plaintext:
            if self._is_alpha(ch):
                ascii_offset = 65 if self._is_upper(ch) else 97
                base = ord(self._to_lower(ch)) - ord('a')
                shifted = self._cpp_mod(base + shift, 26)
                ciphertext.append(chr(shifted + ascii_offset))
            else:
                ciphertext.append(ch)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plain_text: str) -> str:
        encrypted_text = []
        key_index = 0
        key_len = len(self.key)
        for ch in plain_text:
            if self._is_alpha(ch):
                shift = ord(self._to_lower(self.key[key_index % key_len])) - ord('a')
                base = ord(self._to_lower(ch)) - ord('a')
                encrypted_char = chr(self._cpp_mod(base + shift, 26) + ord('a'))
                if self._is_upper(ch):
                    encrypted_text.append(self._to_upper(encrypted_char))
                else:
                    encrypted_text.append(encrypted_char)
                key_index += 1
            else:
                encrypted_text.append(ch)
        return ''.join(encrypted_text)

    def rail_fence_cipher(self, plain_text: str, rails: int) -> str:
        if rails <= 0:
            raise ValueError("Rails must be greater than zero.")
        N = 101
        fence = [""] * N
        direction = -1
        row = 0
        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row] += ch
            row += direction
        encrypted_text = []
        for i in range(rails):
            encrypted_text.append(fence[i])
        return ''.join(encrypted_text)