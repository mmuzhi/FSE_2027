import re
from typing import Callable, Dict, List, Tuple


class WordFrequency:
    """Immutable (word, frequency) pair; mirrors the Java inner class."""

    __slots__ = ("word", "frequency")

    def __init__(self, word: str, frequency: int) -> None:
        self.word = word
        self.frequency = frequency

    def get_word(self) -> str:
        return self.word

    def get_frequency(self) -> int:
        return self.frequency

    def __repr__(self) -> str:
        return f"WordFrequency{{word='{self.word}', frequency={self.frequency}}}"

    __str__ = __repr__

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if type(other) is not WordFrequency:
            return False
        return self.frequency == other.frequency and self.word == other.word

    def __hash__(self) -> int:
        return hash((self.word, self.frequency))

    @staticmethod
    def by_frequency_then_word() -> Callable[["WordFrequency"], Tuple[int, str]]:
        """Python equivalent of the Java comparator: frequency desc, then word asc."""
        return lambda wf: (-wf.frequency, wf.word)


# Java's \s is ASCII-only: exactly [ \t\n\x0B\f\r] — keep that, not Python's Unicode \s.
_JAVA_WS = r" \t\n\v\f\r"
_STRIP_PATTERN = re.compile("[^a-zA-Z" + _JAVA_WS + "]")
_SPLIT_PATTERN = re.compile("[" + _JAVA_WS + "]+")


class NLPDataProcessor2:

    def process_data(self, string_list: List[str]) -> List[List[str]]:
        words_list: List[List[str]] = []
        for string in string_list:
            processed_string = _STRIP_PATTERN.sub("", string.lower())
            if not processed_string:
                words: List[str] = []
            else:
                # Emulate Java's String.split("\\s+"): identical segmentation
                # plus Java's dropping of trailing empty strings.
                words = _SPLIT_PATTERN.split(processed_string)
                while words and words[-1] == "":
                    words.pop()
            words_list.append(words)
        return words_list

    def calculate_word_frequency(
        self, words_list: List[List[str]]
    ) -> List[WordFrequency]:
        frequency_map: Dict[str, int] = {}  # insertion-ordered, like LinkedHashMap
        order_map: Dict[str, int] = {}
        index = 0

        for words in words_list:
            for word in words:
                if word not in frequency_map:
                    order_map[word] = index
                    index += 1
                frequency_map[word] = frequency_map.get(word, 0) + 1

        word_frequencies: List[WordFrequency] = []
        for word, frequency in frequency_map.items():
            if frequency > 1 or word == "%%%":
                word_frequencies.append(WordFrequency(word, frequency))

        # Java sort: frequency descending, then first-seen insertion order ascending.
        word_frequencies.sort(key=lambda wf: (-wf.frequency, order_map[wf.word]))
        return word_frequencies

    def process(self, string_list: List[str]) -> List[WordFrequency]:
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)