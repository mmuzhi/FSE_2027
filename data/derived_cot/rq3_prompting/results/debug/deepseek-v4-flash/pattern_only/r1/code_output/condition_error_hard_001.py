from typing import List

class Solution:
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        backward = {word[::-1]: i for i, word in enumerate(words)}
        res = []

        for i, word in enumerate(words):
            if word in backward and backward[word] != i:
                res.append([i, backward[word]])

            if word != "" and "" in backward and word == word[::-1]:
                res.append([i, backward[""]])
                res.append([backward[""], i])

            for j in range(1, len(word)):
                prefix = word[:j]
                suffix = word[j:]

                if suffix in backward and prefix == prefix[::-1] and backward[suffix] != i:
                    res.append([backward[suffix], i])

                if prefix in backward and suffix == suffix[::-1] and backward[prefix] != i:
                    res.append([i, backward[prefix]])

        return res