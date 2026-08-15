from typing import List
from collections import Counter

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        word_len = len(words[0])
        word_count = len(words)
        total_len = word_len * word_count
        target = Counter(words)
        ans = []

        for offset in range(word_len):
            window = Counter()

            for i in range(offset, len(s) - word_len + 1, word_len):
                word = s[i:i + word_len]
                window[word] += 1

                if i >= offset + total_len:
                    old_start = i - total_len
                    old_word = s[old_start:old_start + word_len]
                    window[old_word] -= 1
                    if window[old_word] == 0:
                        del window[old_word]

                if i >= offset + total_len - word_len:
                    if window == target:
                        ans.append(i - total_len + word_len)

        return ans