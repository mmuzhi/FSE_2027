from typing import List
import collections

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        wlen = len(words[0])
        slen = wlen * len(words)
        occ = collections.Counter(words)
        track = {word: 0 for word in occ}
        res = []

        def test() -> bool:
            return all(track[w] == occ[w] for w in occ)

        for k in range(wlen):
            for w in occ:
                track[w] = 0

            for i in range(k, slen + k, wlen):
                w = s[i:i + wlen]
                if w in occ:
                    track[w] += 1

            if test():
                res.append(k)

            for i in range(wlen + k, len(s) - slen + 1, wlen):
                nw = s[i + slen - wlen:i + slen]
                pw = s[i - wlen:i]

                if nw in occ:
                    track[nw] += 1
                if pw in occ:
                    track[pw] -= 1

                if test():
                    res.append(i)

        return res