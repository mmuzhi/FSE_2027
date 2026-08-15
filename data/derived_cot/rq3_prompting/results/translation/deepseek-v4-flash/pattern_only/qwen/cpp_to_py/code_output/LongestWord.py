import string

class LongestWord:
    def __init__(self):
        self.word_list = []

    def add_word(self, word):
        self.word_list.append(word)

    def find_longest_word(self, sentence):
        longest_word = ""
        # ASCII-only lowercase to match C++ std::tolower in the C locale
        lower_sentence = sentence.translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"
        ))
        # Remove ASCII punctuation, matching std::ispunct in the C locale
        lower_sentence = ''.join(ch for ch in lower_sentence if ch not in string.punctuation)

        for word in lower_sentence.split():
            if word in self.word_list and len(word) > len(longest_word):
                longest_word = word

        return longest_word

    def get_word_list(self):
        return self.word_list.copy()