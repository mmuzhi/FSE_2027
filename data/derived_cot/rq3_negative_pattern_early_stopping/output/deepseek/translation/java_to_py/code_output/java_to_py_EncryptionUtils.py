class EncryptionUtils:
    def __init__(self, key: str):
        self.key = key

    def _java_mod(self, a: int, b: int) -> int:
        """
        Returns the remainder with the same sign as the dividend (like Java's %).
        """
        rem = a % b
        if a < 0 and rem != 0:
            rem -= b
        return rem

    def caesar_cipher(self, plaintext: str, shift: int) -> str:
        ciphertext = []
        for c in plaintext:
            if c.isalpha():
                ascii_offset = ord('A') if c.isupper() else ord('a')
                shifted = self._java_mod(ord(c) - ascii_offset + shift, 26) + ascii_offset
                ciphertext.append(chr(shifted))
            else:
                ciphertext.append(c)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plain_text: str) -> str:
        encrypted_text = []
        key_index = 0
        key_lower = self.key.lower()
        key_len = len(key_lower)
        for c in plain_text:
            if c.isalpha():
                shift = ord(key_lower[key_index % key_len]) - ord('a')
                base = ord('a') if c.islower() else ord('A')
                encrypted_char = chr((ord(c.lower()) - ord('a') + shift) % 26 + ord('a'))
                if c.isupper():
                    encrypted_char = encrypted_char.upper()
                encrypted_text.append(encrypted_char)
                key_index += 1
            else:
                encrypted_text.append(c)
        return ''.join(encrypted_text)

    def rail_fence_cipher(self, plain_text: str, rails: int) -> str:
        fence = [['\n' for _ in range(len(plain_text))] for _ in range(rails)]

        direction = -1
        row = 0
        col = 0

        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row][col] = ch
            col += 1
            row += direction

        encrypted_text = []
        for i in range(rails):
            for j in range(len(plain_text)):
                if fence[i][j] != '\n':
                    encrypted_text.append(fence[i][j])
        return ''.join(encrypted_text)