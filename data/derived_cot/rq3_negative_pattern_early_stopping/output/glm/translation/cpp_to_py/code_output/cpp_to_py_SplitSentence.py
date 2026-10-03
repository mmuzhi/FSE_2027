import re


class SplitSentence:
    def split_sentences(self, sentences_string):
        regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"
        parts = re.split(regex, sentences_string, flags=re.ASCII)

        sentences = []
        for sentence in parts:
            if sentence:
                sentence = sentence.rstrip(' \t\n\r\f\v')
                if sentence:
                    sentences.append(sentence)

        return sentences

    def count_words(self, sentence):
        cleaned_sentence = ''.join(
            c for c in sentence
            if c.isascii() and (c.isalpha() or c.isspace())
        )

        words = cleaned_sentence.split()
        return len(words)

    def process_text_file(self, sentences_string):
        sentences = self.split_sentences(sentences_string)
        max_count = 0

        for sentence in sentences:
            count = self.count_words(sentence)
            if count > max_count:
                max_count = count

        return max_count