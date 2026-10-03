class Solution:
    def decodeCiphertext(self, encoded_text: str, rows: int) -> str:
        if rows == 1:
            return encoded_text

        N = len(encoded_text)
        cols = N // rows
        original_text = []

        for j in range(cols):
            i = 0
            curr_j = j
            while i < rows and curr_j < cols:
                original_text.append(encoded_text[i * cols + curr_j])
                i += 1
                curr_j += 1

        return ''.join(original_text).rstrip()