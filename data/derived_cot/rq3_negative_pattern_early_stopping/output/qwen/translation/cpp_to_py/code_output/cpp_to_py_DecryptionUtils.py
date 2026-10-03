class DecryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_decipher(self, ciphertext, shift):
        shift %= 26
        plaintext = []
        for c in ciphertext:
            if c.isalpha():
                base = 'A' if c.isupper() else 'a'
                shifted_char = chr((ord(c) - ord(base) - shift + 26) % 26 + ord(base))
                plaintext.append(shifted_char)
            else:
                plaintext.append(c)
        return ''.join(plaintext)

    def vigenere_decipher(self, ciphertext):
        decrypted_text = []
        key_length = len(self.key)
        key_index = 0
        for c in ciphertext:
            if c.isalpha():
                shift = ord(self.key[key_index % key_length].lower()) - ord('a')
                base_char = c.lower()
                decrypted_char = chr((ord(base_char) - ord('a') - shift + 26) % 26 + ord('a'))
                if c.isupper():
                    decrypted_char = decrypted_char.upper()
                decrypted_text.append(decrypted_char)
                key_index += 1
            else:
                decrypted_text.append(c)
        return ''.join(decrypted_text)

    def rail_fence_decipher(self, encrypted_text, rails):
        n = len(encrypted_text)
        if rails <= 1 or n == 0:
            return encrypted_text

        fence = [''] * rails
        direction = -1
        row, col = 0, 0

        # Mark positions with '*'
        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction *= -1
            fence[row] += '*'
            row += direction

        # Place characters from encrypted_text into the fence
        index = 0
        for r in range(rails):
            for c_pos in range(n):
                if fence[r][c_pos] == '*':
                    fence[r] = fence[r][:c_pos] + encrypted_text[index] + fence[r][c_pos+1:]
                    index += 1

        # Reconstruct plaintext
        direction = -1
        row, col = 0, 0
        plaintext = []
        for _ in range(n):
            if row == 0 or row == rails - 1:
                direction *= -1
            plaintext.append(fence[row][col])
            col += 1
            row += direction

        return ''.join(plaintext)