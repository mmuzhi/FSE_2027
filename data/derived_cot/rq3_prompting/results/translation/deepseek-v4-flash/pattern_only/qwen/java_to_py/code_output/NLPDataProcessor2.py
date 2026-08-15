import re


class _WordFrequencyComparator:
    def compare(self, a, b):
        if a.frequency != b.frequency:
            return b.frequency - a.frequency
        return (a.word > b.word) - (a.word < b.word)

    def __call__(self, wf):
        return (-wf.frequency, wf.word)


class NLPDataProcessor2:
    class WordFrequency:
        def __init__(self, word, frequency):
            self._word = word
            self._frequency = frequency

        @property
        def word(self):
            return self._word

        @property
        def frequency(self):
            return self._frequency

        def getWord(self):
            return self._word

        def getFrequency(self):
            return self._frequency

        def __repr__(self):
            return f"WordFrequency{{word='{self._word}', frequency={self._frequency}}}"

        __str__ = __repr__

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(other) is not NLPDataProcessor2.WordFrequency:
                return False
            return self._frequency == other._frequency and self._word == other._word

        def __hash__(self):
            return hash((self._word, self._frequency))

        @staticmethod
        def byFrequencyThenWord():
            return _WordFrequencyComparator()

    @staticmethod
    def _java_split_whitespace(s):
        parts = re.split(r'\s+', s, flags=re.ASCII)
        while parts and parts[-1] == '':
            parts.pop()
        return parts

    def processData(self, stringList):
        wordsList = []
        pattern = re.compile(r'[^a-zA-Z\s]', re.ASCII)
        for string in stringList:
            processedString = pattern.sub('', string.lower())
            words = self._java_split_whitespace(processedString)
            wordsList.append(words)
        return wordsList

    def calculateWordFrequency(self, wordsList):
        frequencyMap = {}
        orderMap = {}
        index = 0

        for words in wordsList:
            for word in words:
                if word not in frequencyMap:
                    orderMap[word] = index
                    index += 1
                frequencyMap[word] = frequencyMap.get(word, 0) + 1

        wordFrequencies = []
        for word, frequency in frequencyMap.items():
            if frequency > 1 or word == "%%%":
                wordFrequencies.append(self.WordFrequency(word, frequency))

        wordFrequencies.sort(key=lambda wf: (-wf.frequency, orderMap[wf.word]))
        return wordFrequencies

    def process(self, stringList):
        wordsList = self.processData(stringList)
        return self.calculateWordFrequency(wordsList)