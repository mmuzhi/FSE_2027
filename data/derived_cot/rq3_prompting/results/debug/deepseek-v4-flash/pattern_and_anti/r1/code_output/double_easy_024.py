class Solution:
    def sortString(self, s: str) -> str:
        freq = {}
        letters = sorted(set(s))
        res = ""

        for ch in s:
            if ch in freq:
                freq[ch] += 1
            else:
                freq[ch] = 1

        while freq:
            for ch in letters:
                if ch in freq:
                    if freq[ch] > 0:
                        res += ch
                        freq[ch] -= 1
                    if freq[ch] == 0:
                        del freq[ch]

            for ch in letters[::-1]:
                if ch in freq:
                    if freq[ch] > 0:
                        res += ch
                        freq[ch] -= 1
                    if freq[ch] == 0:
                        del freq[ch]

        return res