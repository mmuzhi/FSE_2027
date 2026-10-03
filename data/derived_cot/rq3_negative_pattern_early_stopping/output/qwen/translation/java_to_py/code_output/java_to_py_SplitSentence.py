import re

class SplitSentence:

    def split_sentences(self, sentences_string):
        pattern = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"
        matches = re.finditer(pattern, sentences_string)
        sentences = []
        start = 0
        for match in matches:
            end = match.start()
            sentence = sentences_string[start:end]
            sentences.append(sentence)
            start = match.end()
        remaining = sentences_string[start:]
        if remaining:
            sentences.append(remaining)
        return sentences

    def count_words(self, sentence):
        cleaned = re.sub(r'[^a-zA-Z\s]', '', sentence)
        words = cleaned.split()
        return len(words)

    def process_text_file(self, sentences_string):
        sentences = self.split_sentences(sentences_string)
        max_count = 0
        for sentence in sentences:
            word_count = self.count_words(sentence)
            if word_count > max_count:
                max_count = word_count
        return max_count