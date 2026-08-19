import re


class SplitSentence:
    _SPLIT_RE = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    _WHITESPACE = ' \t\n\v\f\r'  # matches std::isspace in the default C locale

    def split_sentences(self, sentences_string):
        sentences = []
        for sentence in self._SPLIT_RE.split(sentences_string):
            sentence = sentence.rstrip(self._WHITESPACE)
            if sentence:
                sentences.append(sentence)
        return sentences

    def count_words(self, sentence):
        cleaned_sentence = ''.join(
            c for c in sentence if c.isalpha() or c in self._WHITESPACE
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