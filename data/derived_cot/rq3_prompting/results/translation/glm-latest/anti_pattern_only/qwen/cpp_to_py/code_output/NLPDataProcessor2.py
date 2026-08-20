import re


def to_lowercase(string):
    return string.lower()


def remove_non_alpha(string):
    return ''.join(char for char in string if char.isalpha() or char.isspace())


first_appear = {}


class NLPDataProcessor2:

    def process_data(self, string_list):
        words_list = []
        for string in string_list:
            processed_string = to_lowercase(remove_non_alpha(string))
            # Split on whitespace runs and drop empty tokens (as the C++ token iterator + empty check does)
            words = [word for word in re.split(r'\s+', processed_string) if word]
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list):
        word_frequency = {}
        first_appear.clear()
        js = 0
        for words in words_list:
            for word in words:
                if word not in word_frequency:
                    js += 1
                    first_appear[word] = js
                word_frequency[word] = word_frequency.get(word, 0) + 1

        # Equivalent to the C++ comparator: descending count, ties broken by
        # ascending first-appearance index (indices are unique per word).
        sorted_word_frequency = sorted(
            word_frequency.items(),
            key=lambda item: (-item[1], first_appear[item[0]])
        )

        # std::map iterates in key-sorted order, so insert keys alphabetically.
        top_5_word_frequency = {}
        for word, count in sorted(sorted_word_frequency[:5]):
            top_5_word_frequency[word] = count

        return top_5_word_frequency

    def process(self, string_list):
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)