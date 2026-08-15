class NLPDataProcessor:
    def constructStopWordList(self):
        return ["a", "an", "the"]

    def removeStopWords(self, stringList, stopWordList):
        result = []
        for string in stringList:
            words = string.split(' ')
            if string.endswith(' '):
                words.pop()
            words = [word for word in words if word not in stopWordList]
            result.append(words)
        return result

    def process(self, stringList):
        stopWordList = self.constructStopWordList()
        return self.removeStopWords(stringList, stopWordList)