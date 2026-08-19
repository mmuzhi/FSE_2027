class Solution:
    def decodeCiphertext(self, encoded_text: str, rows: int) -> str:
        if rows == 1:
            return encoded_text.rstrip()

        N = len(encoded_text)
        cols = N // rows
        i, j, k = 0, 0, 0
        original_text = []

        while j < cols:
            original_text.append(encoded_text[k])
            i += 1
            if i == rows or i + j == cols:
                i = 0
                j += 1
            k = i * (cols + 1) + j

        return ''.join(original_text).rstrip()