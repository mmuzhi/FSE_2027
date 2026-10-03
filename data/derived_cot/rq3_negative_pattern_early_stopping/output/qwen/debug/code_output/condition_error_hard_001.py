class Solution:
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        backward = {}
        for i, word in enumerate(words):
            reversed_word = word[::-1]
            if reversed_word not in backward:
                backward[reversed_word] = []
            backward[reversed_word].append(i)
        
        res = []
        n = len(words)
        
        for i, word in enumerate(words):
            m = len(word)
            # Case 1: The current word is a palindrome. Then we can pair it with the empty string if it exists.
            if word == "":
                continue
            
            # Case 2: The current word is the first part. We split the word into two parts: prefix and suffix.
            # For each split, if the prefix is a palindrome, then the suffix should be the reverse of some word in the backward map.
            for j in range(m + 1):
                prefix = word[:j]
                suffix = word[j:]
                
                # If the prefix is a palindrome, then we can pair the current word with the reversed of the suffix.
                if prefix == prefix[::-1]:
                    # If the suffix is not empty, we need to find the reversed of the suffix in the backward map.
                    if suffix in backward:
                        for idx in backward[suffix]:
                            if idx != i:
                                res.append([i, idx])
                
                # If the suffix is a palindrome, then we can pair the current word with the reversed of the prefix.
                if suffix == suffix[::-1]:
                    # If the prefix is not empty, we need to find the reversed of the prefix in the backward map.
                    if prefix and prefix in backward:
                        for idx in backward[prefix]:
                            if idx != i:
                                res.append([idx, i])
        
        return res