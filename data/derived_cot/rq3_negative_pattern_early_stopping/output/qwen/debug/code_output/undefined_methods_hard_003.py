class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        # If there are no forbidden words, the answer is the entire string.
        if not forbidden:
            return len(word)
        
        # Convert forbidden list to a set for quick substring check
        forbidden_set = set(forbidden)
        n = len(word)
        max_len = 0
        
        # Iterate over all possible substrings
        for i in range(n):
            # We'll extend j from i to n-1
            for j in range(i, n):
                substr = word[i:j+1]
                # Check if substr contains any forbidden substring
                found = False
                for f in forbidden_set:
                    if f in substr:
                        found = True
                        break
                if not found:
                    max_len = max(max_len, j-i+1)
                else:
                    # Once we find a forbidden substring, we can break early because extending j further will not make the substring valid.
                    # But note: the forbidden substring might be found in the middle, but extending j might add characters that make it invalid, but we are already invalid.
                    # However, we can break out of the inner loop because any longer substring starting at i will be invalid.
                    # But wait, what if the forbidden substring is not at the beginning? We are checking from i to j, and if we find one, then the substring is invalid. But we are already at j, so we can continue to the next i.
                    # But note: the substring might be invalid at a certain j, but valid at a shorter j? But we are iterating j from i to n-1, so we want the longest valid substring starting at i.
                    # We cannot break the inner loop because we are looking for the longest valid substring starting at i. But if we find a forbidden substring at j, then the substring from i to j is invalid, but the substring from i to j-1 might be valid. But we already checked j-1 in the previous iteration.
                    # So we can continue.
                    pass
        
        return max_len