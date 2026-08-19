class Solution:
    def arrayStringsAreEqual(self, word1: List[str], word2: List[str]) -> bool:
        word3 = self.concat(word1)
        word4 = self.concat(word2)
        if word3 == word4:
            return True
        else:
            return False

    def concat(self, word: List[str]) -> str:
        return ''.join(word)