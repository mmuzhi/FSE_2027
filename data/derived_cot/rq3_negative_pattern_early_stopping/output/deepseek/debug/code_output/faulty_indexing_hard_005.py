from typing import List
import collections

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:  # edge case
            return []
        wlen = len(words[0])
        slen = wlen * len(words)
        occ = collections.Counter(words)
        res = []

        for k in range(wlen):
            track = {word: 0 for word in occ}
            for i in range(k, k + slen, wlen):
                w = s[i:i+wlen]
                if w in track:
                    track[w] += 1
            if track == occ:
                res.append(k)
            for start in range(k + wlen, len(s) - slen + 1, wlen):
                pw = s[start - wlen:start]
                if pw in track:
                    track[pw] -= 1
                nw = s[start + slen - wlen:start + slen]
                if nw in track:
                    track[nw] += 1
                if track == occ:
                    res.append(start)
        return res