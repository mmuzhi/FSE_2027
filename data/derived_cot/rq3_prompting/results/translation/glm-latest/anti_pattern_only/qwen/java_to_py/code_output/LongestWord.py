import re


class LongestWord:
    def __init__(self):
        self.wordList = []

    def addWord(self, word):
        self.wordList.append(word)

    def findLongestWord(self, sentence):
        longestWord = ""
        sentence = sentence.lower()
        sentence = re.sub(
            "[" + re.escape("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~") + "]", "", sentence
        )
        words = sentence.split(" ")
        for word in words:
            if word in self.wordList and len(word) > len(longestWord):
                longestWord = word
        return longestWord


if __name__ == "__main__":
    longestWord = LongestWord()
    longestWord.addWord("A")
    longestWord.addWord("aM")
    print(longestWord.findLongestWord("I am a student."))