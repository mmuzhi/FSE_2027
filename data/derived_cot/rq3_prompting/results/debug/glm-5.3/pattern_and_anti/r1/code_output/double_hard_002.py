import collections
from typing import List


class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        wlen = len(words[0])
        slen = wlen * len(words)
        track = dict()
        occ = collections.Counter(words)

        def test():
            for key, val in track.items():
                if val != occ[key]:
                    return False
            return True

        res = []

        for k in range(wlen):
            for word in words:
                track.update({word: 0})
            for i in range(k, slen + k, wlen):
                w = s[i:i + wlen]
                if w in words:
                    track.update({w: track[w] + 1})
            if test():
                res.append(k)
            # slide the window by wlen steps
            for i in range(wlen + k, len(s) - slen + 1, wlen):
                nw = s[i + slen - wlen:i + slen]
                pw = s[i - wlen:i]
                if nw in words:
                    track.update({nw: track[nw] + 1})
                if pw in words:
                    track.update({pw: track[pw] - 1})
                if test():
                    res.append(i)
        return res