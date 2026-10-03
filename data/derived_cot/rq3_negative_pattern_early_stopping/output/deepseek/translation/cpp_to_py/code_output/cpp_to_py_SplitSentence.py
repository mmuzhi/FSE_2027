import re
import string

class SplitSentence:
    def split_sentences(self, sentences_string: str):
        pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?!])\s'
        sentences = re.split(pattern, sentences_string)
        result = []
        for s in sentences:
            s = s.rstrip()
            if s:
                result.append(s)
        return result

    def count_words(self, sentence: str) -> int:
        cleaned = ''.join(c for c in sentence if c.isalpha() or c.isspace())
        words = cleaned.split()
        return len(words)

    def process_text_file(self, sentences_string: str) -> int:
        sentences = self.split_sentences(sentences_string)
        max_count = 0
        for s in sentences:
            count = self.count_words(s)
            if count > max_count:
                max_count = count
        return max_count