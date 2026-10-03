class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        # If there are no forbidden words, the entire word is valid.
        if not forbidden:
            return len(word)
        
        # Build a set of forbidden words for quick lookup
        forbidden_set = set(forbidden)
        n = len(word)
        max_len = 0
        
        # Iterate over all starting positions
        for i in range(n):
            # We'll check substrings starting at i
            found = False
            for j in range(i, n):
                # Check if the substring word[i:j+1] contains any forbidden word
                substr = word[i:j+1]
                for forb in forbidden_set:
                    if forb in substr:
                        # Found a forbidden substring, so the valid substring ending at j-1 has length j-i
                        max_len = max(max_len, j - i)
                        found = True
                        break
                if found:
                    break
            else:
                # If we didn't break, then the entire substring from i to the end is valid
                max_len = max(max_len, n - i)
                
        return max_len