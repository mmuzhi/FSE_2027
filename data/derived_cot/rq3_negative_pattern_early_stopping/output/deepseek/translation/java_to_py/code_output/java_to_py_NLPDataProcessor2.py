import re
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

@dataclass(unsafe_hash=True, order=False)
class WordFrequency:
    word: str
    frequency: int

    def __repr__(self) -> str:
        return f"WordFrequency{{word='{self.word}', frequency={self.frequency}}}"

    @staticmethod
    def by_frequency_then_word() -> 'key':
        def key(wf: 'WordFrequency') -> Tuple:
            return (-wf.frequency, wf.word)
        return key


class NLPDataProcessor2:
    def process_data(self, string_list: List[str]) -> List[List[str]]:
        result = []
        pattern = re.compile(r'[^a-zA-Z\s]')
        for s in string_list:
            processed = pattern.sub('', s.lower())
            if not processed:
                result.append([])
            else:
                words = processed.split()
                result.append(words)
        return result

    def calculate_word_frequency(self, words_list: List[List[str]]) -> List[WordFrequency]:
        frequency: Dict[str, int] = {}
        order: Dict[str, int] = {}
        index = 0

        for words in words_list:
            for word in words:
                if word not in frequency:
                    order[word] = index
                    index += 1
                frequency[word] = frequency.get(word, 0) + 1

        wf_list: List[WordFrequency] = []
        for word, freq in frequency.items():
            if freq > 1 or word == '%%%':
                wf_list.append(WordFrequency(word, freq))

        wf_list.sort(key=lambda wf: (-wf.frequency, order[wf.word]))
        return wf_list

    def process(self, string_list: List[str]) -> List[WordFrequency]:
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)