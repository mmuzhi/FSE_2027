import collections
from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not words:
            return []
        wlen = len(words[0])
        slen = wlen * len(words)
        if slen > len(s):
            return []
        track = dict()
        
        occ = collections.Counter(words)

        def test():
            for key, val in track.items():
                if val != occ[key]:
                    return False
            return True
            
        res = []
        
        for k in range(wlen):
            for i in words:
                track[i] = 0
            for i in range(k, slen + k, wlen):
                w = s[i:i + wlen]
                if w in occ:
                    track[w] = track.get(w, 0) + 1
            if test():
                res.append(k)
            for i in range(wlen + k, len(s) - slen + 1, wlen):
                nw = s[i + slen - wlen:i + slen]
                pw = s[i - wlen:i]
                if nw in occ:
                    track[nw] = track.get(nw, 0) + 1
                if pw in occ:
                    track[pw] = track.get(pw, 0) - 1
                if test():
                    res.append(i)
        return res