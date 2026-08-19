class DecryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_decipher(self, ciphertext, shift):
        shift = shift % 26
        plaintext = []
        for c in ciphertext:
            if ('a' <= c <= 'z') or ('A' <= c <= 'Z'):
                base = ord('A') if 'A' <= c <= 'Z' else ord('a')
                plaintext.append(chr((ord(c) - base - shift + 26) % 26 + base))
            else:
                plaintext.append(c)
        return ''.join(plaintext)

    def vigenere_decipher(self, ciphertext):
        decrypted_text = []
        key_length = len(self.key)
        key_index = 0

        for c in ciphertext:
            if ('a' <= c <= 'z') or ('A' <= c <= 'Z'):
                k_ord = ord(self.key[key_index % key_length])
                if ord('A') <= k_ord <= ord('Z'):
                    k_ord += 32
                shift = k_ord - ord('a')

                c_low = ord(c)
                if ord('A') <= c_low <= ord('Z'):
                    c_low += 32
                decrypted_char = chr((c_low - ord('a') - shift + 26) % 26 + ord('a'))
                if 'A' <= c <= 'Z':
                    decrypted_char = decrypted_char.upper()
                decrypted_text.append(decrypted_char)
                key_index += 1
            else:
                decrypted_text.append(c)
        return ''.join(decrypted_text)

    def rail_fence_decipher(self, encrypted_text, rails):
        n = len(encrypted_text)
        if rails <= 1:
            return encrypted_text

        fence = [['\n'] * n for _ in range(rails)]

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