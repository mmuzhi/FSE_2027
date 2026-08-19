class NLPDataProcessor:

    def construct_stop_word_list(self):
        return ["a", "an", "the"]

    def remove_stop_words(self, string_list, stop_word_list):
        result = []
        for string in string_list:
            words = string.split(" ")
            # Java's String.split(" ") drops trailing empty strings; Python keeps them.
            while len(words) > 1 and words[-1] == "":
                words.pop()
            words = [w for w in words if w not in stop_word_list]  # removeAll
            result.append(words)
        return result

    def process(self, string_list):
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)