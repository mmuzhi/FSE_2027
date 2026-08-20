import re
import string

# Mappings that reproduce the default "C" locale behavior of the original
# C++ code (::tolower, std::ispunct, and istringstream whitespace handling).
_TO_LOWER = str.maketrans(string.ascii_uppercase, string.ascii_lowercase)
_DROP_PUNCT = str.maketrans("", "", string.punctuation)
_C_WHITESPACE = re.compile(r"[ \t\n\v\f\r]+")


class LongestWord:
    def __init__(self):
        self.word_list = []

    def add_word(self, word):
        self.word_list.append(word)

    def find_longest_word(self, sentence):
        longest_word = ""

        # ::tolower — only ASCII uppercase letters are lowercased.
        lower_sentence = sentence.translate(_TO_LOWER)

        # std::ispunct — ASCII punctuation characters are erased.
        lower_sentence = lower_sentence.translate(_DROP_PUNCT)

        # `stream >> word` — extract words separated by whitespace
        # (leading/trailing/repeated whitespace yields no empty words).
        for word in (w for w in _C_WHITESPACE.split(lower_sentence) if w):
            if word in self.word_list and len(word) > len(longest_word):
                longest_word = word

        return longest_word

    def get_word_list(self):
        return list(self.word_list)