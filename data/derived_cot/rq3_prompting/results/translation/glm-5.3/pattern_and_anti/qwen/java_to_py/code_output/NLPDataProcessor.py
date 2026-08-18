class NLPDataProcessor:

    def construct_stop_word_list(self):
        return ["a", "an", "the"]

    @staticmethod
    def _java_split(string):
        # Java's String.split(" ") discards trailing empty strings,
        # except for empty input, which yields [""].
        if string == "":
            return [""]
        parts = string.split(" ")
        while parts and parts[-1] == "":
            parts.pop()
        return parts

    def remove_stop_words(self, string_list, stop_word_list):
        result = []
        for string in string_list:
            words = [w for w in self._java_split(string) if w not in stop_word_list]
            result.append(words)
        return result

    def process(self, string_list):
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)