class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def _java_mod(a, b):
        # Java's % truncates toward zero (sign of dividend), unlike Python's %
        r = a % b
        if a < 0 and r != 0:
            r -= b
        return r

    def caesarCipher(self, plaintext, shift):
        ciphertext = []
        for c in plaintext:
            if c.isalpha():
                ascii_offset = ord('A') if c.isupper() else ord('a')
                shifted = chr(self._java_mod(ord(c) - ascii_offset + shift, 26) + ascii_offset)
                ciphertext.append(shifted)
            else:
                ciphertext.append(c)
        return ''.join(ciphertext)

    def vigenereCipher(self, plain_text):
        encrypted_text = []
        key_index = 0
        for c in plain_text:
            if c.isalpha():
                shift = ord(self.key[key_index % len(self.key)].lower()) - ord('a')
                encrypted_char = chr(self._java_mod(ord(c.lower()) - ord('a') + shift, 26) + ord('a'))
                encrypted_text.append(encrypted_char.upper() if c.isupper() else encrypted_char)
                key_index += 1
            else:
                encrypted_text.append(c)
        return ''.join(encrypted_text)

    def railFenceCipher(self, plain_text, rails):
        fence = [['\n'] * len(plain_text) for _ in range(rails)]

        direction = -1
        row, col = 0, 0

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