class Solution:
    def decodeCiphertext(self, encoded_text: str, rows: int) -> str:
        if rows == 1:
            return encoded_text
        
        N = len(encoded_text)
        cols = N // rows
        original_text = []
        
        for j in range(cols):
            for i in range(rows):
                original_text.append(encoded_text[j * rows + i])
        
        return ''.join(original_text)
