class Solution:
    def sortString(self, s: str) -> str:
        freq = {}
        for ch in s:
            freq[ch] = freq.get(ch, 0) + 1
        letters = sorted(freq.keys())
        res = []
        while freq:
            for ch in letters:
                if ch in freq:
                    res.append(ch)
                    freq[ch] -= 1
                    if freq[ch] == 0:
                        del freq[ch]
            for ch in reversed(letters):
                if ch in freq:
                    res.append(ch)
                    freq[ch] -= 1
                    if freq[ch] == 0:
                        del freq[ch]
        return ''.join(res)