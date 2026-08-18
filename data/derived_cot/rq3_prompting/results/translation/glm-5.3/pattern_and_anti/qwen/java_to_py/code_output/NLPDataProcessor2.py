import re
from dataclasses import dataclass
from typing import Callable, List


@dataclass(frozen=True)
class WordFrequency:
    word: str
    frequency: int

    def __str__(self) -> str:
        return f"WordFrequency{{word='{self.word}', frequency={self.frequency}}}"

    @staticmethod
    def by_frequency_then_word() -> Callable[["WordFrequency"], tuple]:
        # Comparator.comparingInt(frequency).reversed().thenComparing(word)
        return lambda wf: (-wf.frequency, wf.word)


class NLPDataProcessor2:
    # Java's \s is exactly [ \t\n\x0B\f\r]; keep the same class to avoid
    # Python's Unicode-wider \s semantics.
    _NON_WORD = re.compile(r"[^a-zA-Z \t\n\x0b\f\r]")
    _WHITESPACE = re.compile(r"[ \t\n\x0b\f\r]+")

    def process_data(self, string_list: List[str]) -> List[List[str]]:
        words_list: List[List[str]] = []
        for string in string_list:
            processed_string = self._NON_WORD.sub("", string.lower())
            if processed_string == "":
                words = []
            else:
                words = self._WHITESPACE.split(processed_string)
                # Java's String.split drops trailing empty strings; re.split does not.
                while words and words[-1] == "":
                    words.pop()
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list: List[List[str]]) -> List[WordFrequency]:
        frequency_map = {}  # insertion-ordered, like LinkedHashMap
        order_map = {}
        index = 0

        for words in words_list:
            for word in words:
                if word not in frequency_map:
                    order_map[word] = index
                    index += 1
                frequency_map[word] = frequency_map.get(word, 0) + 1

        word_frequencies = []
        for word, frequency in frequency_map.items():
            if frequency > 1 or word == "%%%":
                word_frequencies.append(WordFrequency(word, frequency))

        # frequency desc, then first-appearance order asc
        word_frequencies.sort(key=lambda wf: (-wf.frequency, order_map[wf.word]))
        return word_frequencies

    def process(self, string_list: List[str]) -> List[WordFrequency]:
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)