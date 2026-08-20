class NLPDataProcessor:

    def construct_stop_word_list(self):
        return ["a", "an", "the"]

    @staticmethod
    def _split_like_java(string):
        # Mimics Java's String.split(" "): trailing empty strings are
        # dropped, and if the separator never occurs the whole string is
        # returned as a single element (so "" -> [""]).
        if " " not in string:
            return [string]
        words = string.split(" ")
        while words and words[-1] == "":
            words.pop()
        return words

    def remove_stop_words(self, string_list, stop_word_list):
        result = []
        for string in string_list:
            words = [word for word in self._split_like_java(string)
                     if word not in stop_word_list]
            result.append(words)
        return result

    def process(self, string_list):
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)