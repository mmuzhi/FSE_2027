class Solution:
    def decodeCiphertext(self, encoded_text: str, rows: int) -> str:
        n = len(encoded_text)
        cols = n // rows
        res = []

        for start_col in range(cols):
            r, c = 0, start_col
            while r < rows and c < cols:
                res.append(encoded_text[r * cols + c])
                r += 1
                c += 1

        return ''.join(res).rstrip()