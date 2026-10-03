import string

class LongestWord:
    def __init__(self):
        self.word_list = []

    def add_word(self, word):
        self.word_list.append(word)

    def find_longest_word(self, sentence):
        lower_sentence = sentence.lower()
        lower_sentence = lower_sentence.translate(str.maketrans('', '', string.punctuation))
        
        longest_word = ""
        for word in lower_sentence.split():
            if word in self.word_list and len(word) > len(longest_word):
                longest_word = word
        return longest_word

    def get_word_list(self):
        return self.word_list