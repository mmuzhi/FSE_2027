class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        ciphertext = []
        for ch in plaintext:
            if ch.isalpha():
                base = 'a' if ch.islower() else 'A'
                shifted_char = chr(((ord(ch.lower()) - ord('a') + shift) % 26) + ord('a'))
                if ch.isupper():
                    shifted_char = shifted_char.upper()
                ciphertext.append(shifted_char)
            else:
                ciphertext.append(ch)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plain_text):
        encrypted_text = []
        key_index = 0
        for ch in plain_text:
            if ch.isalpha():
                shift = ord(self.key[key_index % len(self.key)].lower()) - ord('a')
                shifted_char = chr(((ord(ch.lower()) - ord('a') + shift) % 26) + ord('a'))
                if ch.isupper():
                    shifted_char = shifted_char.upper()
                encrypted_text.append(shifted_char)
                key_index += 1
            else:
                encrypted_text.append(ch)
        return ''.join(encrypted_text)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 0:
            raise ValueError("Rails must be greater than zero.")
        fence = [''] * rails
        direction = -1
        row = 0
        for ch in plain_text:
            fence[row] += ch
            if row == 0 or row == rails - 1:
                direction *= -1
            row += direction
        return ''.join(fence)