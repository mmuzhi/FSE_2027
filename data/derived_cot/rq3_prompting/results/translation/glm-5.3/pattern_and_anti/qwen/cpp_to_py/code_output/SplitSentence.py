import re

# Mirrors the C locale classification used by std::isspace / std::isalpha
_ASCII_WHITESPACE = ' \t\n\v\f\r'
_ASCII_LETTERS = frozenset(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
)

_SENTENCE_SPLIT_RE = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')


class SplitSentence:
    def split_sentences(self, sentences_string):
        sentences = []

        for sentence in _SENTENCE_SPLIT_RE.split(sentences_string):
            if sentence:
                # Equivalent of erase(find_if(rbegin, rend, not space).base(), end):
                # strip trailing whitespace only (right-trim).
                end = len(sentence)
                while end > 0 and sentence[end - 1] in _ASCII_WHITESPACE:
                    end -= 1
                sentence = sentence[:end]
                if sentence:
                    sentences.append(sentence)

        return sentences

    def count_words(self, sentence):
        cleaned_sentence = ''.join(
            c for c in sentence
            if c in _ASCII_LETTERS or c in _ASCII_WHITESPACE
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