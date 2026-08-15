import collections
from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        wlen = len(words[0])
        slen = wlen * len(words)
        occ = collections.Counter(words)
        res = []

        def matches(track):
            return track == occ

        for k in range(wlen):
            track = {word: 0 for word in words}

            for i in range(k, slen + k, wlen):
                w = s[i:i + wlen]
                if w in occ:
                    track[w] += 1

            if matches(track):
                res.append(k)

            for i in range(wlen + k, len(s) - slen + 1, wlen):
                nw = s[i + slen - wlen:i + slen]
                pw = s[i - wlen:i]

                if nw in occ:
                    track[nw] += 1
                if pw in occ:
                    track[pw] -= 1

                if matches(track):
                    res.append(i)

        return sorted(res)