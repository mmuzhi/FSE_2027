from typing import List
import collections

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not words or not s:
            return []
        wlen = len(words[0])
        slen = wlen * len(words)
        if len(s) < slen:
            return []
        occ = collections.Counter(words)
        res = []

        def test(track):
            for key, val in track.items():
                if val != occ[key]:
                    return False
            return True

        for k in range(wlen):
            track = {word: 0 for word in words}
            for i in range(k, k + slen, wlen):
                w = s[i:i + wlen]
                if w in words:
                    track[w] += 1
            if test(track):
                res.append(k)
            for i in range(k + wlen, len(s) - slen + 1, wlen):
                pw = s[i - wlen:i]
                nw = s[i + slen - wlen:i + slen]
                if pw in words:
                    track[pw] -= 1
                if nw in words:
                    track[nw] += 1
                if test(track):
                    res.append(i)
        return res