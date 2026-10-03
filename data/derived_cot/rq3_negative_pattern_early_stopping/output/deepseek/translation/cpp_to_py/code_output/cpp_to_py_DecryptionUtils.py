class DecryptionUtils:
    def __init__(self, key: str):
        self.key_ = key

    def caesar_decipher(self, ciphertext: str, shift: int) -> str:
        shift = shift % 26
        plaintext = []
        for c in ciphertext:
            if c.isalpha():
                base = ord('A') if c.isupper() else ord('a')
                shifted = (ord(c) - base - shift + 26) % 26 + base
                plaintext.append(chr(shifted))
            else:
                plaintext.append(c)
        return ''.join(plaintext)

    def vigenere_decipher(self, ciphertext: str) -> str:
        decrypted = []
        key_len = len(self.key_)
        key_idx = 0
        for c in ciphertext:
            if c.isalpha():
                shift = ord(self.key_[key_idx % key_len].lower()) - ord('a')
                dec_lower = chr((ord(c.lower()) - ord('a') - shift + 26) % 26 + ord('a'))
                if c.isupper():
                    decrypted.append(dec_lower.upper())
                else:
                    decrypted.append(dec_lower)
                key_idx += 1
            else:
                decrypted.append(c)
        return ''.join(decrypted)

    def rail_fence_decipher(self, encrypted_text: str, rails: int) -> str:
        n = len(encrypted_text)
        if rails <= 1:
            return encrypted_text
        fence = [['\n' for _ in range(n)] for _ in range(rails)]
        row, col = 0, 0
        direction = -1
        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row][col] = '*'
            col += 1
            row += direction
        idx = 0
        for r in range(rails):
            for c in range(n):
                if fence[r][c] == '*':
                    fence[r][c] = encrypted_text[idx]
                    idx += 1
        plain = []
        row, col = 0, 0
        direction = -1
        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction = -direction
            plain.append(fence[row][col])
            col += 1
            row += direction
        return ''.join(plain)