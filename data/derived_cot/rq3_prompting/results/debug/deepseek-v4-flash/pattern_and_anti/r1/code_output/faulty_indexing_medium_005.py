class Solution:
    def decodeCiphertext(self, encoded_text: str, rows: int) -> str:
        n = len(encoded_text)
        cols = n // rows
        original_text = []

        for j in range(cols):
            for i in range(rows):
                idx = i * (cols + 1) + j
                if idx < n:
                    original_text.append(encoded_text[idx])

        return ''.join(original_text).rstrip()