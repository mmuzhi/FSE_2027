class NLPDataProcessor:
    def construct_stop_word_list(self):
        return ["a", "an", "the"]

    def remove_stop_words(self, string_list, stop_word_list):
        answer = []
        for s in string_list:
            words = s.split()
            filtered = []
            for word in words:
                if word not in stop_word_list:
                    filtered.append(word)
            answer.append(filtered)
        return answer

    def process(self, string_list):
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)