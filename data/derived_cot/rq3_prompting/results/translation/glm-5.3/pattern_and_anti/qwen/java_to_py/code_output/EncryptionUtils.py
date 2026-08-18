class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def _java_mod(a, b):
        # Java's % truncates toward zero (sign of dividend), and int ops wrap to 32 bits.
        a = ((a + 0x80000000) & 0xFFFFFFFF) - 0x80000000
        r = a % b
        return r - b if a < 0 and r != 0 else r

    @staticmethod
    def _is_letter(c):
        # Character.isLetter sees only UTF-16 code units (<= U+FFFF)
        return c.isalpha() and ord(c) <= 0xFFFF

    @staticmethod
    def _to_lower(c):
        # Character.toLowerCase is a simple (1:1) mapping
        lc = c.lower()
        return lc if len(lc) == 1 else lc[0]

    def caesar_cipher(self, plaintext, shift):
        ciphertext = []
        for c in plaintext:
            if self._is_letter(c):
                ascii_offset = ord('A') if c.isupper() else ord('a')
                shifted_char = chr(self._java_mod(ord(c) - ascii_offset + shift, 26) + ascii_offset)
                ciphertext.append(shifted_char)
            else:
                ciphertext.append(c)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plain_text):
        encrypted_text = []
        key_index = 0
        for c in plain_text:
            if self._is_letter(c):
                shift = ord(self._to_lower(self.key[key_index % len(self.key)])) - ord('a')
                encrypted_char = chr(self._java_mod(ord(self._to_lower(c)) - ord('a') + shift, 26) + ord('a'))
                encrypted_text.append(encrypted_char.upper() if c.isupper() else encrypted_char)
                key_index += 1
            else:
                encrypted_text.append(c)
        return ''.join(encrypted_text)

    def rail_fence_cipher(self, plain_text, rails):
        if rails < 0:
            raise IndexError("rails < 0: %d" % rails)  # NegativeArraySizeException analog
        fence = [['\n'] * len(plain_text) for _ in range(rails)]

        direction = -1
        row = 0
        col = 0

        for c in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction

            fence[row][col] = c
            col += 1
            row += direction

        encrypted_text = []
        for i in range(rails):
            for j in range(len(plain_text)):
                if fence[i][j] != '\n':
                    encrypted_text.append(fence[i][j])
        return ''.join(encrypted_text)