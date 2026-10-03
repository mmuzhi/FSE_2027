import re
from typing import List, Dict, OrderedDict, Tuple
from functools import cmp_to_key

class NLPDataProcessor2:

    class WordFrequency:
        def __init__(self, word: str, frequency: int):
            self.word = word
            self.frequency = frequency

        def __repr__(self):
            return f"WordFrequency(word='{self.word}', frequency={self.frequency})"

        def __eq__(self, other):
            if not isinstance(other, NLPDataProcessor2.WordFrequency):
                return False
            return self.word == other.word and self.frequency == other.frequency

        def __hash__(self):
            return hash((self.word, self.frequency))

        @classmethod
        def by_frequency_then_word(cls) -> Tuple:
            # This comparator is used for sorting by frequency descending and then word ascending.
            # But note: the Java comparator returns reversed frequency then word.
            # We can define a comparator function and then use cmp_to_key.
            def compare(wf1, wf2):
                # Compare by frequency descending
                if wf1.frequency != wf2.frequency:
                    return wf2.frequency - wf1.frequency  # descending
                # Then by word (ascending)
                return wf1.word.compareTo(wf2.word)  # In Python, we use the natural order of strings
            return cmp_to_key(compare)

    def process_data(self, string_list: List[str]) -> List[List[str]]:
        # Compile the regex pattern to remove non-alphanumeric and non-space characters
        pattern = re.compile(r'[^a-zA-Z\s]')
        words_list = []
        for string in string_list:
            # Convert to lowercase and remove non-alphanumeric and non-space
            processed_string = pattern.sub('', string.lower())
            # If the processed string is empty, return an empty list for this string
            if processed_string == '':
                words_list.append([])
            else:
                # Split by whitespace and create a list of words
                words_list.append(processed_string.split())
        return words_list

    def calculate_word_frequency(self, words_list: List[List[str]]) -> List['NLPDataProcessor2.WordFrequency']:
        # We'll use dictionaries to keep track of frequencies and the order of appearance
        frequency_map: Dict[str, int] = {}
        order_map: Dict[str, int] = {}  # This will map word to its index (order of first occurrence)
        index = 0

        # First, we need to go through all the words and record the first occurrence and update frequency
        for words in words_list:
            for word in words:
                # If we haven't seen the word before, record its order
                if word not in order_map:
                    order_map[word] = index
                    index += 1
                # Update the frequency
                frequency_map[word] = frequency_map.get(word, 0) + 1

        # Now, create a list of WordFrequency for words that appear more than once OR the word is "%%%"
        word_frequencies = []
        for word, freq in frequency_map.items():
            if freq > 1 or word == "%%%":
                word_frequencies.append(NLPDataProcessor2.WordFrequency(word, freq))

        # Sort the word_frequencies by frequency descending and then by the order (index) ascending
        # We use the comparator defined in WordFrequency
        word_frequencies.sort(key=cmp_to_key(NLPDataProcessor2.WordFrequency.by_frequency_then_word()))
        return word_frequencies

    def process(self, string_list: List[str]) -> List['NLPDataProcessor2.WordFrequency']:
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)