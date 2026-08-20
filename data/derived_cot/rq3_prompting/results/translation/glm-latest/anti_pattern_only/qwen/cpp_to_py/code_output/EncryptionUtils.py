def _is_alpha(ch):
    # std::isalpha with the default "C" locale: ASCII letters only.
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z'


def _is_upper(ch):
    # std::isupper with the default "C" locale.
    return 'A' <= ch <= 'Z'


def _to_lower(ch):
    # std::tolower with the default "C" locale.
    return chr(ord(ch) + 32) if 'A' <= ch <= 'Z' else ch


def _to_upper(ch):
    # std::toupper with the default "C" locale.
    return chr(ord(ch) - 32) if 'a' <= ch <= 'z' else ch


def _cpp_mod(value, mod):
    # C++ integer % truncates toward zero (remainder keeps the dividend's sign),
    # unlike Python's floored modulo. Needed for negative shifts / odd key chars.
    result = value % mod
    if value < 0 and result != 0:
        result -= mod
    return result


class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        ciphertext = []
        for ch in plaintext:
            if _is_alpha(ch):
                ascii_offset = 65 if _is_upper(ch) else 97
                shifted_char = chr(
                    _cpp_mod(ord(_to_lower(ch)) - ord('a') + shift, 26) + ascii_offset
                )
                ciphertext.append(shifted_char)
            else:
                ciphertext.append(ch)
        return ''.join(ciphertext)

    def vigenere_cipher(self, plain_text):
        encrypted_text = []
        key_index = 0
        key_length = len(self.key)
        for ch in plain_text:
            if _is_alpha(ch):
                shift = ord(_to_lower(self.key[key_index % key_length])) - ord('a')
                encrypted_char = chr(
                    _cpp_mod(ord(_to_lower(ch)) - ord('a') + shift, 26) + ord('a')
                )
                encrypted_text.append(
                    _to_upper(encrypted_char) if _is_upper(ch) else encrypted_char
                )
                key_index += 1
            else:
                encrypted_text.append(ch)
        return ''.join(encrypted_text)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 0:
            raise ValueError("Rails must be greater than zero.")
        N = 101
        fence = [''] * N
        direction = -1
        row = 0

        for ch in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction

            fence[row] += ch
            row += direction

        encrypted_text = ''
        for i in range(rails):
            encrypted_text += fence[i]

        return encrypted_text