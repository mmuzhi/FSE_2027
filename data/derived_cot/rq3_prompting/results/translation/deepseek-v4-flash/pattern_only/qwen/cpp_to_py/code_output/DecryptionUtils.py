class DecryptionUtils:
    def __init__(self, key: str):
        self.key_ = key

    def caesar_decipher(self, ciphertext: str, shift: int) -> str:
        shift = shift % 26
        plaintext = []
        for c in ciphertext:
            if self._is_alpha(c):
                base = 'A' if self._is_upper(c) else 'a'
                shifted_char = chr((ord(c) - ord(base) - shift + 26) % 26 + ord(base))
                plaintext.append(shifted_char)
            else:
                plaintext.append(c)
        return ''.join(plaintext)

    def vigenere_decipher(self, ciphertext: str) -> str:
        decrypted_text = []
        key_length = len(self.key_)
        key_index = 0

        for c in ciphertext:
            if self._is_alpha(c):
                shift = ord(self._to_lower(self.key_[key_index % key_length])) - ord('a')
                decrypted_char = chr((ord(self._to_lower(c)) - ord('a') - shift + 26) % 26 + ord('a'))
                if self._is_upper(c):
                    decrypted_text.append(self._to_upper(decrypted_char))
                else:
                    decrypted_text.append(decrypted_char)
                key_index += 1
            else:
                decrypted_text.append(c)

        return ''.join(decrypted_text)

    def rail_fence_decipher(self, encrypted_text: str, rails: int) -> str:
        n = len(encrypted_text)
        if rails <= 1:
            return encrypted_text

        fence = [['\n' for _ in range(n)] for _ in range(rails)]

        direction = -1
        row = 0
        col = 0

        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row][col] = '*'
            col += 1
            row += direction

        index = 0
        for r in range(rails):
            for c in range(n):
                if fence[r][c] == '*':
                    fence[r][c] = encrypted_text[index]
                    index += 1

        direction = -1
        row = 0
        col = 0
        plain_text = []

        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction = -direction
            plain_text.append(fence[row][col])
            col += 1
            row += direction

        return ''.join(plain_text)

    @staticmethod
    def _is_alpha(c: str) -> bool:
        return ('A' <= c <= 'Z') or ('a' <= c <= 'z')

    @staticmethod
    def _is_upper(c: str) -> bool:
        return 'A' <= c <= 'Z'

    @staticmethod
    def _is_lower(c: str) -> bool:
        return 'a' <= c <= 'z'

    @staticmethod
    def _to_lower(c: str) -> str:
        if 'A' <= c <= 'Z':
            return chr(ord(c) + 32)
        return c

    @staticmethod
    def _to_upper(c: str) -> str:
        if 'a' <= c <= 'z':
            return chr(ord(c) - 32)
        return c