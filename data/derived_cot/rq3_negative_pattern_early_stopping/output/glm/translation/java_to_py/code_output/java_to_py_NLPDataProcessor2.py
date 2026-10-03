import re
from functools import cmp_to_key

class NLPDataProcessor2:

    class WordFrequency:
        def __init__(self, word, frequency):
            self.word = word
            self.frequency = frequency

        def getWord(self):
            return self.word

        def getFrequency(self):
            return self.frequency

        def __repr__(self):
            return f"WordFrequency{{word='{self.word}', frequency={self.frequency}}}"

        def __eq__(self, o):
            if self is o:
                return True
            if o is None or type(o) != NLPDataProcessor2.WordFrequency:
                return False
            return self.frequency == o.frequency and self.word == o.word

        def __hash__(self):
            return hash((self.word, self.frequency))

        @staticmethod
        def byFrequencyThenWord():
            def compare(wf1, wf2):
                freq_cmp = wf2.getFrequency() - wf1.getFrequency()
                if freq_cmp != 0:
                    return freq_cmp
                if wf1.getWord() < wf2.getWord():
                    return -1
                elif wf1.getWord() > wf2.getWord():
                    return 1
                return 0
            return cmp_to_key(compare)

    def processData(self, string_list):
        words_list = []
        pattern = re.compile(r'[^a-zA-Z\s]')

        for string in string_list:
            processed_string = pattern.sub('', string.lower())
            if not processed_string:
                words = []
            else:
                words = re.split(r'\s+', processed_string)
                while words and words[-1] == '':
                    words.pop()
            words_list.append(words)
        return words_list

    def calculateWordFrequency(self, words_list):
        frequency_map = {}
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
                word_frequencies.append(NLPDataProcessor2.WordFrequency(word, frequency))

        word_frequencies.sort(key=lambda wf: (-wf.frequency, order_map[wf.word]))

        return word_frequencies

    def process(self, string_list):
        words_list = self.processData(string_list)
        return self.calculateWordFrequency(words_list)