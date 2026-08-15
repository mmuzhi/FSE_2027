class EncryptionUtils:
    def __init__(self, key: str):
        self.key = key

    def _is_alpha(self, ch: str) -> bool:
        return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')

    def _is_upper(self, ch: str) -> bool:
        return 'A' <= ch <= 'Z'

    def _to_lower(self, ch: str) -> str:
        if 'A' <= ch <= 'Z':
            return chr(ord(ch) + 32)
        return ch

    def _to_upper(self, ch: str) -> str:
        if 'a' <= ch <= 'z':
            return chr(ord(ch) - 32)
        return ch

    def _cpp_mod(self, a: int, b: int) -> int:
        r = a % b
        if r != 0 and a < 0:
            r -= b
        return r

    def caesar_cipher(self, plaintext: str, shift: int) -> str:
        ciphertext = []
        for ch in plaintext:
            if self._is_alpha(ch):
                ascii_offset = 65 if self._is_upper(ch) else 97
                shifted = self._cpp_mod(ord(self._to_lower(ch)) - ord('a') + shift, 26)
                shifted_char = chr(shifted + ascii_offset)
                ciphertext.append(shifted_char)
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
                encrypted_char = chr(self._cpp_mod(ord(self._to_lower(ch)) - ord('a') + shift, 26) + ord('a'))
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
        fence = ["" for _ in range(101)]
        direction = -1
        row = 0

        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row] += ch
            row += direction

        return ''.join(fence[i] for i in range(rails))