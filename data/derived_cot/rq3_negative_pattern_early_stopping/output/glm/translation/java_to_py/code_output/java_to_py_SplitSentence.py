import re

class SplitSentence:

    def split_sentences(self, sentences_string):
        sentences = []
        pattern = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")
        last_end = 0
        
        for matcher in pattern.finditer(sentences_string):
            sentences.append(sentences_string[last_end:matcher.end() - 1])
            last_end = matcher.end()
            
        if last_end < len(sentences_string):
            sentences.append(sentences_string[last_end:])
            
        return sentences

    def count_words(self, sentence):
        cleaned_sentence = re.sub(r'[^a-zA-Z\s]', '', sentence)
        
        if cleaned_sentence == "":
            return 1
            
        words = re.split(r'\s+', cleaned_sentence)
        
        while words and words[-1] == '':
            words.pop()
            
        return len(words)

    def process_text_file(self, sentences_string):
        sentences = self.split_sentences(sentences_string)
        return max((self.count_words(s) for s in sentences), default=0)