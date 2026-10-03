import re


class SplitSentence:
    def split_sentences(self, sentences_string):
        pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
        matches = re.findall(pattern, sentences_string)
        sentences = []
        for match in matches:
            trimmed = match.rstrip()
            if trimmed:
                sentences.append(trimmed)
        return sentences

    def count_words(self, sentence):
        cleaned = ''.join(filter(lambda c: c.isalpha() or c.isspace(), sentence))
        words = cleaned.split()
        return len(words)

    def process_text_file(self, sentences_string):
        sentences = self.split_sentences(sentences_string)
        max_count = 0
        for sent in sentences:
            cnt = self.count_words(sent)
            if cnt > max_count:
                max_count = cnt
        return max_count