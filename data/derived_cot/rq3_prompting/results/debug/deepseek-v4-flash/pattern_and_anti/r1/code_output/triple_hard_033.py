from typing import List
from collections import Counter

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        wlen = len(words[0])
        slen = wlen * len(words)

        if slen > len(s):
            return []

        occ = Counter(words)
        res = []

        def test(track):
            for key, val in occ.items():
                if track.get(key, 0) != val:
                    return False
            return True

        for k in range(wlen):
            if k + slen > len(s):
                continue

            track = {word: 0 for word in words}

            for i in range(k, k + slen, wlen):
                w = s[i:i + wlen]
                if w in occ:
                    track[w] += 1

            if test(track):
                res.append(k)

            for i in range(k + wlen, len(s) - slen + 1, wlen):
                nw = s[i + slen - wlen:i + slen]
                pw = s[i - wlen:i]

                if nw in occ:
                    track[nw] += 1
                if pw in occ:
                    track[pw] -= 1

                if test(track):
                    res.append(i)

        return res