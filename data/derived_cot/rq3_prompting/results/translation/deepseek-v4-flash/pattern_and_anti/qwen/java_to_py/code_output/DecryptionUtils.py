class DecryptionUtils:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def _to_utf16_units(s):
        units = []
        for ch in s:
            cp = ord(ch)
            if cp > 0xFFFF:
                cp -= 0x10000
                units.append(chr(0xD800 + (cp >> 10)))
                units.append(chr(0xDC00 + (cp & 0x3FF)))
            else:
                units.append(ch)
        return units

    @staticmethod
    def _java_mod26(a):
        if a >= 0:
            return a % 26
        else:
            return -((-a) % 26)

    def caesarDecipher(self, ciphertext, shift):
        shift = self._java_mod26(shift)
        plaintext = []
        for ch in self._to_utf16_units(ciphertext):
            if ch.isalpha():
                ascii_offset = ord('A') if ch.isupper() else ord('a')
                shifted = chr(self._java_mod26(ord(ch) - ascii_offset - shift + 26) + ascii_offset)
                plaintext.append(shifted)
            else:
                plaintext.append(ch)
        return ''.join(plaintext)

    def vigenereDecipher(self, ciphertext):
        decrypted = []
        key_units = self._to_utf16_units(self.key)
        key_index = 0
        for ch in self._to_utf16_units(ciphertext):
            if ch.isalpha():
                shift = ord(key_units[key_index % len(key_units)].lower()) - ord('a')
                base = ord('A') if ch.isupper() else ord('a')
                decrypted_char = chr(self._java_mod26(ord(ch) - base - shift + 26) + base)
                decrypted.append(decrypted_char)
                key_index += 1
            else:
                decrypted.append(ch)
        return ''.join(decrypted)

    def railFenceDecipher(self, encryptedText, rails):
        units = self._to_utf16_units(encryptedText)
        n = len(units)
        fence = [['\0'] * n for _ in range(rails)]

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
        for i in range(rails):
            for j in range(n):
                if fence[i][j] == '*':
                    fence[i][j] = units[index]
                    index += 1

        plain_text = []
        direction = -1
        row = 0
        col = 0

        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction = -direction
            plain_text.append(fence[row][col])
            col += 1
            row += direction

        return ''.join(plain_text)