class Solution:
    def decodeCiphertext(self, encoded_text: str, rows: int) -> str:
        if rows == 1:
            return encoded_text

        N = len(encoded_text)
        cols = N // rows
        grid = [[''] * cols for _ in range(rows)]
        idx = 0

        for start_col in range(cols):
            i, j = 0, start_col
            while i < rows and j < cols:
                grid[i][j] = encoded_text[idx]
                idx += 1
                i += 1
                j += 1

        original = []
        for i in range(rows):
            for j in range(cols):
                original.append(grid[i][j])

        return ''.join(original).rstrip()