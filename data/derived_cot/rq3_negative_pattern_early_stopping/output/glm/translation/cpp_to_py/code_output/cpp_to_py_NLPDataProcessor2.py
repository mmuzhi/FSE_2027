import re


class NLPDataProcessor2:
    _first_appear = {}

    def process_data(self, string_list):
        words_list = []
        for s in string_list:
            processed_string = _to_lowercase(_remove_non_alpha(s))
            words = [w for w in re.split(r'\s+', processed_string) if w]
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list):
        word_frequency = {}
        NLPDataProcessor2._first_appear.clear()
        js = 0
        for words in words_list:
            for word in words:
                if word not in word_frequency:
                    js += 1
                    NLPDataProcessor2._first_appear[word] = js
                word_frequency[word] = word_frequency.get(word, 0) + 1

        sorted_word_frequency = sorted(
            word_frequency.items(),
            key=lambda x: (-x[1], NLPDataProcessor2._first_appear[x[0]])
        )

        top_5 = sorted_word_frequency[:5]
        top_5_word_frequency = {}
        for key, value in sorted(top_5, key=lambda x: x[0]):
            top_5_word_frequency[key] = value

        return top_5_word_frequency

    def process(self, string_list):
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)


def _to_lowercase(s):
    return s.lower()


def _remove_non_alpha(s):
    result = []
    for c in s:
        if c.isalpha() or c.isspace():
            result.append(c)
    return ''.join(result)