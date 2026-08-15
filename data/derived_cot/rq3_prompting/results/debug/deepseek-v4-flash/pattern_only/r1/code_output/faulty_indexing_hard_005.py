from typing import List
import collections

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        wlen = len(words[0])
        slen = wlen * len(words)
        occ = collections.Counter(words)
        res = []

        for k in range(wlen):
            track = {word: 0 for word in occ}

            for i in range(k, slen + k, wlen):
                w = s[i:i + wlen]
                if w in occ:
                    track[w] += 1

            if track == occ:
                res.append(k)

            for i in range(wlen + k, len(s) - slen + 1, wlen):
                nw = s[i + slen - wlen:i + slen]
                pw = s[i - wlen:i]

                if nw in occ:
                    track[nw] += 1
                if pw in occ:
                    track[pw] -= 1

                if track == occ:
                    res.append(i)

        return sorted(res)