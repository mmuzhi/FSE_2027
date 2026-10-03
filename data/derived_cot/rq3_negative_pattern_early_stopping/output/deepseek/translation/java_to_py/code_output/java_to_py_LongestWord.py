class LongestWord:
    def __init__(self):
        self.wordList = []

    def addWord(self, word):
        self.wordList.append(word)

    def findLongestWord(self, sentence):
        longest_word = ""

        sentence = sentence.lower()

        punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        sentence = sentence.translate(str.maketrans('', '', punctuation))

        words = sentence.split(' ')

        for word in words:
            if word in self.wordList and len(word) > len(longest_word):
                longest_word = word

        return longest_word


if __name__ == "__main__":
    obj = LongestWord()
    obj.addWord("A")
    obj.addWord("aM")
    print(obj.findLongestWord("I am a student."))