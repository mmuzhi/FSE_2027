import re
from typing import List, Dict, Tuple

class NLPDataProcessor2:
    def process_data(self, string_list: List[str]) -> List[List[str]]:
        words_list = []
        for s in string_list:
            processed = []
            for ch in s:
                if ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ch == ' ' or ch == '\t' or ch == '\n' or ch == '\r' or ch == '\f' or ch == '\v':
                    processed.append(ch)
            processed_str = ''.join(processed).lower()
            words = processed_str.split()
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list: List[List[str]]) -> Dict[str, int]:
        word_frequency = {}
        first_appear = {}
        idx = 0
        for words in words_list:
            for word in words:
                if word not in word_frequency:
                    idx += 1
                    first_appear[word] = idx
                word_frequency[word] = word_frequency.get(word, 0) + 1

        sorted_words = sorted(word_frequency.items(), key=lambda x: (-x[1], first_appear[x[0]]))
        top5 = {}
        for word, freq in sorted_words[:5]:
            top5[word] = freq
        return top5

    def process(self, string_list: List[str]) -> Dict[str, int]:
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)