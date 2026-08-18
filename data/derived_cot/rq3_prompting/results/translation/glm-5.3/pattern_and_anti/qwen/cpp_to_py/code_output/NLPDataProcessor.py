class NLPDataProcessor:
    def construct_stop_word_list(self):
        return ["a", "an", "the"]

    def remove_stop_words(self, string_list, stop_word_list):
        answer = []
        for s in string_list:
            string_split = [word for word in s.split() if word not in stop_word_list]
            answer.append(string_split)
        return answer

    def process(self, string_list):
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)