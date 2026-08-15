class NLPDataProcessor:
    def constructStopWordList(self):
        return ["a", "an", "the"]

    def removeStopWords(self, stringList, stopWordList):
        result = []
        for string in stringList:
            words = string.split(" ")
            while len(words) > 1 and words[-1] == "":
                words.pop()
            result.append([word for word in words if word not in stopWordList])
        return result

    def process(self, stringList):
        return self.removeStopWords(stringList, self.constructStopWordList())