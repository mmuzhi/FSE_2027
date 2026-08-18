import re


class SplitSentence:
    # Mirrors Java's default (ASCII) regex semantics:
    # \s == [ \t\n\x0B\f\r], \w == [a-zA-Z0-9_],
    # and '.' matches any char except \n \r \u0085 \u2028 \u2029.
    _PATTERN = re.compile(
        r'(?<!\w\.\w[^\n\r\x85\u2028\u2029])(?<![A-Z][a-z]\.)(?<=\.|\?)\s',
        re.ASCII,
    )

    def split_sentences(self, sentences_string):
        sentences = []
        last_end = 0
        for matcher in self._PATTERN.finditer(sentences_string):
            sentences.append(sentences_string[last_end:matcher.end() - 1])
            last_end = matcher.end()
        if last_end < len(sentences_string):
            sentences.append(sentences_string[last_end:])
        return sentences

    @staticmethod
    def _java_split_word_count(cleaned_sentence):
        # Emulates Java's String.split("\\s+") with limit 0:
        # - no match at all -> [input] (length 1, even for "")
        # - otherwise trailing empty strings are discarded,
        #   but a leading empty string is kept.
        words = re.split(r'\s+', cleaned_sentence, flags=re.ASCII)
        if len(words) == 1:
            return 1
        while words and words[-1] == '':
            words.pop()
        return len(words)

    def count_words(self, sentence):
        cleaned_sentence = re.sub(r'[^a-zA-Z\s]', '', sentence, flags=re.ASCII)
        return self._java_split_word_count(cleaned_sentence)

    def process_text_file(self, sentences_string):
        sentences = self.split_sentences(sentences_string)
        max_count = 0
        for sentence in sentences:
            count = self.count_words(sentence)
            if count > max_count:
                max_count = count
        return max_count