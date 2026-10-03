class Solution:
    def sortString(self, s: str) -> str:
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1
        
        letters = sorted(freq.keys())
        res = []
        
        while freq:
            # Increasing pass
            for char in letters:
                if freq[char] > 0:
                    res.append(char)
                    freq[char] -= 1
                    if freq[char] == 0:
                        del freq[char]
            
            # Decreasing pass
            for char in reversed(letters):
                if freq[char] > 0:
                    res.append(char)
                    freq[char] -= 1
                    if freq[char] == 0:
                        del freq[char]
        
        return "".join(res)
