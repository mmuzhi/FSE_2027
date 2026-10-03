class DecryptionUtils:
    def __init__(self, key: str):
        self.key = key

    def caesarDecipher(self, ciphertext: str, shift: int) -> str:
        plaintext = []
        shift = shift % 26
        for ch in ciphertext:
            if ch.isalpha():
                ascii_offset = ord('A') if ch.isupper() else ord('a')
                shifted_char = chr((ord(ch) - ascii_offset - shift + 26) % 26 + ascii_offset)
                plaintext.append(shifted_char)
            else:
                plaintext.append(ch)
        return ''.join(plaintext)

    def vigenereDecipher(self, ciphertext: str) -> str:
        decrypted_text = []
        key_index = 0
        for ch in ciphertext:
            if ch.isalpha():
                shift = ord(self.key[key_index % len(self.key)].lower()) - ord('a')
                base = ord('A') if ch.isupper() else ord('a')
                decrypted_char = chr((ord(ch) - base - shift + 26) % 26 + base)
                decrypted_text.append(decrypted_char)
                key_index += 1
            else:
                decrypted_text.append(ch)
        return ''.join(decrypted_text)

    def railFenceDecipher(self, encrypted_text: str, rails: int) -> str:
        fence = [['\0'] * len(encrypted_text) for _ in range(rails)]

        direction = -1
        row = 0
        col = 0

        for i in range(len(encrypted_text)):
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row][col] = '*'
            col += 1
            row += direction

        index = 0
        for i in range(rails):
            for j in range(len(encrypted_text)):
                if fence[i][j] == '*':
                    fence[i][j] = encrypted_text[index]
                    index += 1

        plain_text = []
        direction = -1
        row = 0
        col = 0

        for i in range(len(encrypted_text)):
            if row == 0 or row == rails - 1:
                direction = -direction
            plain_text.append(fence[row][col])
            col += 1
            row += direction

        return ''.join(plain_text)