class NLPDataProcessor:
    def construct_stop_word_list(self):
        return ["a", "an", "the"]

    def remove_stop_words(self, string_list, stop_word_list):
        answer = []
        for s in string_list:
            words = []
            for word in s.split():
                if word not in stop_word_list:
                    words.append(word)
            answer.append(words)
        return answer

    def process(self, string_list):
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)