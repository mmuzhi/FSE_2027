class Solution:
    def sortString(self, s: str) -> str:
        freq = {}
        letters = sorted(set(s))
        res = ""
        for i in s:
            if i in freq:
                freq[i]+=1
            else:
                freq[i] = 1
        while freq:
            for i in letters:
                if i in freq:
                    res+=i
                    freq[i]-=1
                    if freq[i] == 0:
                        del freq[i]
                    
            for i in letters[::-1]:
                if i in freq:
                    res+=i
                    freq[i]-=1
                    if freq[i] == 0:
                        del freq[i]

        return res