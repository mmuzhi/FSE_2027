class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        result = []
        for char in plaintext:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shifted_char = chr(((ord(char) - ascii_offset + shift) % 26) + ascii_offset)
                result.append(shifted_char)
            else:
                result.append(char)
        return ''.join(result)

    def vigenere_cipher(self, plain_text):
        encrypted_chars = []
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                shift = ord(self.key[key_index % len(self.key)].lower()) - 97
                shifted_char = chr(((ord(char.lower()) - 97 + shift) % 26) + 97)
                if char.isupper():
                    shifted_char = shifted_char.upper()
                encrypted_chars.append(shifted_char)
                key_index += 1
            else:
                encrypted_chars.append(char)
        return ''.join(encrypted_chars)

    def rail_fence_cipher(self, plain_text, rails):
        if rails == 1:
            return plain_text
        
        fence = [['\n' for _ in range(len(plain_text))] for _ in range(rails)]
        direction = -1
        row, col = 0, 0
        
        for char in plain_text:
            fence[row][col] = char
            if row == 0 or row == rails - 1:
                direction *= -1
            row += direction
            col += 1
        
        encrypted_chars = []
        for i in range(rails):
            for j in range(len(plain_text)):
                if fence[i][j] != '\n':
                    encrypted_chars.append(fence[i][j])
        return ''.join(encrypted_chars)