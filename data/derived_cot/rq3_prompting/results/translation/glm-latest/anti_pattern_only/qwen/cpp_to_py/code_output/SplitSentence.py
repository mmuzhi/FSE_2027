import re


class SplitSentence:
    _SEPARATOR = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")

    def split_sentences(self, sentences_string):
        sentences = []
        for sentence in self._SEPARATOR.split(sentences_string):
            if sentence:
                sentence = sentence.rstrip()
                if sentence:
                    sentences.append(sentence)
        return sentences

    def count_words(self, sentence):
        cleaned_sentence = "".join(
            ch for ch in sentence if ch.isalpha() or ch.isspace()
        )
        return len(cleaned_sentence.split())

    def process_text_file(self, sentences_string):
        sentences = self.split_sentences(sentences_string)
        max_count = 0
        for sentence in sentences:
            count = self.count_words(sentence)
            if count > max_count:
                max_count = count
        return max_count