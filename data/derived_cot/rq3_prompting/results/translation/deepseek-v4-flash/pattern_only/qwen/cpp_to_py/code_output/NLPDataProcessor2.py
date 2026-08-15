def to_lowercase(s):
    return ''.join(chr(ord(c) + 32) if 'A' <= c <= 'Z' else c for c in s)

def remove_non_alpha(s):
    return ''.join(c for c in s if ('A' <= c <= 'Z') or ('a' <= c <= 'z') or c in ' \t\n\v\f\r')

first_appear = {}

class NLPDataProcessor2:
    def process_data(self, string_list):
        words_list = []
        for s in string_list:
            processed = to_lowercase(remove_non_alpha(s))
            words = []
            current = []
            for c in processed:
                if c in ' \t\n\v\f\r':
                    if current:
                        words.append(''.join(current))
                        current = []
                else:
                    current.append(c)
            if current:
                words.append(''.join(current))
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list):
        first_appear.clear()
        word_frequency = {}
        js = 0

        for words in words_list:
            for word in words:
                if word not in word_frequency:
                    js += 1
                    first_appear[word] = js
                    word_frequency[word] = 0
                word_frequency[word] += 1

        sorted_items = sorted(
            word_frequency.items(),
            key=lambda item: (-item[1], first_appear[item[0]])
        )
        top_5 = sorted_items[:5]

        result = {}
        for word, count in sorted(top_5, key=lambda x: x[0]):
            result[word] = count

        # Reorder first_appear to match std::map key iteration order
        items = sorted(first_appear.items())
        first_appear.clear()
        first_appear.update(items)

        return result

    def process(self, string_list):
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)