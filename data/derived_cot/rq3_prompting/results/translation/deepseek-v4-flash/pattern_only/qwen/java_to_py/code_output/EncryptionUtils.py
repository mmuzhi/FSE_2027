class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def _java_mod(a, b):
        r = a % b
        if r != 0 and (a < 0) != (b < 0):
            r -= b
        return r

    def caesarCipher(self, plaintext, shift):
        ciphertext = []
        for c in plaintext:
            if c.isalpha():
                ascii_offset = ord('A') if c.isupper() else ord('a')
                shifted = self._java_mod(ord(c) - ascii_offset + shift, 26) + ascii_offset
                ciphertext.append(chr(shifted))
            else:
                ciphertext.append(c)
        return ''.join(ciphertext)

    def vigenereCipher(self, plainText):
        encryptedText = []
        keyIndex = 0
        for c in plainText:
            if c.isalpha():
                shift = ord(self.key[keyIndex % len(self.key)].lower()) - ord('a')
                encryptedChar = chr(self._java_mod(ord(c.lower()) - ord('a') + shift, 26) + ord('a'))
                encryptedText.append(encryptedChar.upper() if c.isupper() else encryptedChar)
                keyIndex += 1
            else:
                encryptedText.append(c)
        return ''.join(encryptedText)

    def railFenceCipher(self, plainText, rails):
        fence = [['\n' for _ in range(len(plainText))] for _ in range(rails)]
        direction = -1
        row = 0
        col = 0

        for c in plainText:
            if row == 0 or row == rails - 1:
                direction = -direction

            fence[row][col] = c
            col += 1
            row += direction

        encryptedText = []
        for i in range(rails):
            for j in range(len(plainText)):
                if fence[i][j] != '\n':
                    encryptedText.append(fence[i][j])
        return ''.join(encryptedText)