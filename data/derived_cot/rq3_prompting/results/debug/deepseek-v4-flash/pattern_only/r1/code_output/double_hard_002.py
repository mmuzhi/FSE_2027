from typing import List
from collections import Counter

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        word_len = len(words[0])
        total_len = word_len * len(words)

        if len(s) < total_len:
            return []

        target = Counter(words)
        res = []

        def matches(track):
            return all(track.get(word, 0) == target[word] for word in target)

        for k in range(word_len):
            track = {word: 0 for word in target}

            for i in range(k, k + total_len, word_len):
                w = s[i:i + word_len]
                if w in target:
                    track[w] += 1

            if matches(track):
                res.append(k)

            for i in range(k + word_len, len(s) - total_len + 1, word_len):
                add = s[i + total_len - word_len: i + total_len]
                rem = s[i - word_len: i]

                if add in target:
                    track[add] += 1
                if rem in target:
                    track[rem] -= 1

                if matches(track):
                    res.append(i)

        return sorted(res)