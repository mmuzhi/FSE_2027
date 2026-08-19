import re


class SplitSentence:
    # Java's default \s and \w are ASCII-only; re.ASCII replicates that.
    _SENTENCE_SPLIT_RE = re.compile(
        r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", re.ASCII
    )
    _CLEAN_RE = re.compile(r"[^a-zA-Z\s]", re.ASCII)
    _WHITESPACE_RE = re.compile(r"\s+", re.ASCII)

    def split_sentences(self, sentences_string):
        sentences = []
        last_end = 0
        for match in self._SENTENCE_SPLIT_RE.finditer(sentences_string):
            sentences.append(sentences_string[last_end:match.end() - 1])
            last_end = match.end()
        if last_end < len(sentences_string):
            sentences.append(sentences_string[last_end:])
        return sentences

    def count_words(self, sentence):
        cleaned_sentence = self._CLEAN_RE.sub("", sentence)
        # Java's split("\\s+") keeps a leading empty string and returns [""]
        # for empty input, but drops trailing empty strings.
        if cleaned_sentence == "":
            return 1
        words = self._WHITESPACE_RE.split(cleaned_sentence)
        while words and words[-1] == "":
            words.pop()
        return len(words)

    def process_text_file(self, sentences_string):
        sentences = self.split_sentences(sentences_string)
        max_count = 0
        for sentence in sentences:
            count = self.count_words(sentence)
            if count > max_count:
                max_count = count
        return max_count