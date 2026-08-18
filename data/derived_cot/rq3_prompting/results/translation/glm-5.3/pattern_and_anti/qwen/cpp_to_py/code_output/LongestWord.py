import string


class LongestWord:
    def __init__(self):
        self._word_list = []

    def add_word(self, word):
        self._word_list.append(word)

    def find_longest_word(self, sentence):
        longest_word = ""
        lower_sentence = sentence.lower()
        lower_sentence = "".join(
            c for c in lower_sentence if c not in string.punctuation
        )
        for word in lower_sentence.split():
            if word in self._word_list and len(word) > len(longest_word):
                longest_word = word
        return longest_word

    def get_word_list(self):
        return list(self._word_list)