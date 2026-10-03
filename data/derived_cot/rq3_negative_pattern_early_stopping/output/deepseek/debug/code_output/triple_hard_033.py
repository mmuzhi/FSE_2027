from typing import List
import collections

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        word_len = len(words[0])
        word_count = len(words)
        total_len = word_len * word_count
        target = collections.Counter(words)
        result = []

        for offset in range(word_len):
            left = offset
            right = offset
            current = collections.Counter()

            while right + word_len <= len(s):
                word = s[right:right + word_len]
                right += word_len

                if word in target:
                    current[word] += 1
                    while current[word] > target[word]:
                        left_word = s[left:left + word_len]
                        current[left_word] -= 1
                        left += word_len

                    if right - left == total_len:
                        result.append(left)
                        left_word = s[left:left + word_len]
                        current[left_word] -= 1
                        left += word_len
                else:
                    current.clear()
                    left = right

        return result