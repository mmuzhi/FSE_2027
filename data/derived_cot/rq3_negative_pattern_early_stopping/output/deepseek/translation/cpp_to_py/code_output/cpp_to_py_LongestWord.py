import string

class LongestWord:
    def __init__(self):
        self.word_list = []

    def add_word(self, word):
        self.word_list.append(word)

    def find_longest_word(self, sentence):
        longest_word = ""
        lower_sentence = sentence.lower()
        translator = str.maketrans('', '', string.punctuation)
        lower_sentence = lower_sentence.translate(translator)
        words = lower_sentence.split()
        for word in words:
            if word in self.word_list and len(word) > len(longest_word):
                longest_word = word
        return longest_word

    def get_word_list(self):
        return list(self.word_list)