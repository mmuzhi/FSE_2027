class Solution:
    def concat(self, words: List[str]) -> str:
        return ''.join(words)

    def arrayStringsAreEqual(self, word1: List[str], word2: List[str]) -> bool:
        word3 = self.concat(word1)
        word4 = self.concat(word2)
        return word3 == word4