class DecryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_decipher(self, ciphertext, shift):
        shift = shift % 26
        plaintext = []
        for char in ciphertext:
            if char.isupper():
                base = 'A'
                shifted_char = chr(((ord(char) - ord(base) - shift) % 26) + ord(base))
                plaintext.append(shifted_char)
            elif char.islower():
                base = 'a'
                shifted_char = chr(((ord(char) - ord(base) - shift) % 26) + ord(base))
                plaintext.append(shifted_char)
            else:
                plaintext.append(char)
        return ''.join(plaintext)

    def vigenere_decipher(self, ciphertext):
        decrypted_text = []
        key_index = 0
        for char in ciphertext:
            if char.isupper():
                base = 'A'
                shift = ord(self.key[key_index % len(self.key)].upper()) - ord('A')
                decrypted_char = chr(((ord(char) - ord(base) - shift) % 26) + ord(base))
                decrypted_text.append(decrypted_char)
                key_index += 1
            elif char.islower():
                base = 'a'
                shift = ord(self.key[key_index % len(self.key)].lower()) - ord('a')
                decrypted_char = chr(((ord(char) - ord(base) - shift) % 26) + ord(base))
                decrypted_text.append(decrypted_char)
                key_index += 1
            else:
                decrypted_text.append(char)
        return ''.join(decrypted_text)

    def rail_fence_decipher(self, encrypted_text, rails):
        if rails == 0 or len(encrypted_text) == 0:
            return encrypted_text

        fence = [['' for _ in range(len(encrypted_text))] for _ in range(rails)]
        direction = -1
        row, col = 0, 0

        # Mark the positions in the fence
        for i in range(len(encrypted_text)):
            if row == 0 or row == rails - 1:
                direction *= -1
            fence[row][col] = '*'
            row += direction
            col += 1

        # Fill the fence with characters
        index = 0
        for i in range(rails):
            for j in range(len(encrypted_text)):
                if fence[i][j] == '*':
                    fence[i][j] = encrypted_text[index]
                    index += 1

        # Reconstruct the plaintext in the same zigzag pattern
        direction = -1
        row, col = 0, 0
        plaintext = []
        for i in range(len(encrypted_text)):
            if row == 0 or row == rails - 1:
                direction *= -1
            plaintext.append(fence[row][col])
            row += direction
            col += 1

        return ''.join(plaintext)