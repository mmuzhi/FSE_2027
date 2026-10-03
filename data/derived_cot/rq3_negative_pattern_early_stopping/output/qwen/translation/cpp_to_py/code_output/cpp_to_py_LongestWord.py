import string

class LongestWord:
    def __init__(self):
        self.word_list = []

    def add_word(self, word):
        self.word_list.append(word)

    def find_longest_word(self, sentence):
        # Convert the sentence to lowercase
        sentence_lower = sentence.lower()
        
        # Remove punctuation
        # We'll remove all punctuation characters from the sentence
        # Create a translation table to remove punctuation, but note: we want to keep letters and spaces
        # Alternatively, we can remove each punctuation character individually
        # Using string.punctuation to get all punctuation characters
        # We'll create a new string without any punctuation
        # But note: the C++ code removes punctuation and then splits, so we want to remove punctuation and keep the rest.
        # We can do: remove all characters that are in string.punctuation
        # However, note that the C++ code uses std::remove_if which removes each punctuation character. We can do the same.
        # Let's remove each punctuation character
        # We can use a set for efficiency, but the sentence might not be huge.
        # Alternatively, we can use a translation table with str.maketrans or use a loop.
        # But note: the C++ code does not remove non-ASCII punctuation? We'll assume ASCII for now.

        # We'll remove all punctuation characters
        # Create a string of punctuation characters
        # Then, remove each occurrence
        # We can do: 
        #   clean_sentence = ''.join(ch for ch in sentence_lower if ch not in string.punctuation)
        clean_sentence = ''.join(ch for ch in sentence_lower if ch not in string.punctuation)
        
        # Now split the clean_sentence into words
        words = clean_sentence.split()

        longest_word = ""
        for word in words:
            # Check if word is in word_list and longer than current longest
            if word in self.word_list and len(word) > len(longest_word):
                longest_word = word

        return longest_word

    def get_word_list(self):
        return self.word_list