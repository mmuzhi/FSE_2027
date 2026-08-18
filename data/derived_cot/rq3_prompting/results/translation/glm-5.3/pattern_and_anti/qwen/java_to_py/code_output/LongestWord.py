import string


class LongestWord:
    def __init__(self):
        self.word_list = []

    def add_word(self, word):
        self.word_list.append(word)

    def find_longest_word(self, sentence):
        longest_word = ""
        sentence = sentence.lower()
        sentence = "".join(ch for ch in sentence if ch not in string.punctuation)
        words = sentence.split(" ")
        for word in words:
            if word in self.word_list and len(word) > len(longest_word):
                longest_word = word
        return longest_word


if __name__ == "__main__":
    longest_word = LongestWord()
    longest_word.add_word("A")
    longest_word.add_word("aM")
    print(longest_word.find_longest_word("I am a student."))