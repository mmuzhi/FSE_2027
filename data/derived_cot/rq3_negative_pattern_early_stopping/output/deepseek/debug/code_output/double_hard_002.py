from typing import List
import collections

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []
        wlen = len(words[0])
        total_len = wlen * len(words)
        occ = collections.Counter(words)
        res = []

        for offset in range(wlen):
            track = {word: 0 for word in words}
            for i in range(offset, offset + total_len, wlen):
                if i + wlen > len(s):
                    break
                w = s[i:i+wlen]
                if w in track:
                    track[w] += 1
            if track == occ:
                res.append(offset)
            for start in range(offset + wlen, len(s) - total_len + 1, wlen):
                new_word = s[start + total_len - wlen: start + total_len]
                if new_word in track:
                    track[new_word] += 1
                old_word = s[start - wlen: start]
                if old_word in track:
                    track[old_word] -= 1
                    if track[old_word] == 0:
                        del track[old_word]  # keep dict clean for comparison
                if track == occ:
                    res.append(start)
        return res