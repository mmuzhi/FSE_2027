import re


class NLPDataProcessor2:
    def process_data(self, string_list):
        words_list = []
        for s in string_list:
            processed = ''.join(c for c in s.lower() if c.isalpha() or c.isspace())
            words = [w for w in re.split(r'\s+', processed) if w != '']
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list):
        word_frequency = {}
        first_appear = {}
        js = 0
        for words in words_list:
            for word in words:
                if word not in word_frequency:
                    js += 1
                    first_appear[word] = js
                word_frequency[word] = word_frequency.get(word, 0) + 1

        sorted_word_frequency = sorted(
            word_frequency.items(),
            key=lambda kv: (-kv[1], first_appear[kv[0]])
        )

        top_5_word_frequency = {}
        for i in range(min(5, len(sorted_word_frequency))):
            top_5_word_frequency[sorted_word_frequency[i][0]] = sorted_word_frequency[i][1]

        return top_5_word_frequency

    def process(self, string_list):
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)