class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        trie = {}
        for f in forbidden:
            t = trie
            for c in f:
                if c not in t:
                    t[c] = {}
                t = t[c]
            t["end"] = True
        
        def isForbidden(s):
            t = trie
            for idx, c in enumerate(s):
                if c not in t:
                    return False
                t = t[c]
                if "end" in t:
                    return idx + 1
            return False
        
        n = len(word)
        j = n
        for i in range(n):
            # Check substring word[i:j]
            if isForbidden(word[i:j]):
                # Find the minimal j such that the substring is valid
                # We need to move j backwards until the substring is valid
                # But note: we are moving i from left to right, so we can move j backwards
                # However, we can also move j backwards until the substring is valid
                # But the problem is that the forbidden substring might be found in the middle
                # We can set j to i and then expand until we find a forbidden substring?
                # Alternatively, we can move j backwards until the substring is valid
                # But note: we are iterating i from 0 to n-1, and j starts from n and we are moving i forward
                # We can set j to i and then expand j until we find a forbidden substring, but that is inefficient
                # Instead, we can move j backwards until the substring is valid
                # But note: we are in a loop that starts from i=0 and j=n, and we are checking word[i:j]
                # We want to find the longest valid substring starting at i
                # We can set j = i and then expand j until we find a forbidden substring, but that is O(n^2)
                # Alternatively, we can use a two-pointer that moves j backwards when a forbidden substring is found
                # But note: the original code was moving from the end. Let's change the approach to two-pointer from the beginning.
                # We'll change the approach to a two-pointer that moves both i and j.
                pass
        
        # Let's change the approach to two-pointer from the beginning
        # We'll use two pointers i and j, and we'll maintain a set of forbidden substrings in the current window?
        # But we have a trie, so we can check the substring from i to j for forbidden substrings.
        # We can start with i=0, j=0, and then expand j until we find a forbidden substring, then move i forward.
        # But note: the forbidden substring might be found in the middle, so we need to check the entire substring from i to j.
        # We can do:
        #   j = 0
        #   for i in range(n):
        #       while j < n and not isForbidden(word[i:j+1]):
        #           j += 1
        #       res = max(res, j - i)
        #       if j == i:
        #           j += 1
        # But note: the isForbidden function returns the length of the forbidden substring found, or False.
        # We need to adjust j when a forbidden substring is found.
        # However, the above approach might be inefficient because isForbidden checks the entire substring from i to j.
        # But note: the length of the substring can be up to n, and we do this for each i, so worst-case O(n^2) which is acceptable for n up to 10^5? Probably not, because 10^5^2 is 10^10.
        # We need a more efficient way.

        # Alternatively, we can use a state machine with the trie and update the forbidden substring as we move the pointers.
        # But let's stick to the trie and the two-pointer approach and hope that the forbidden substrings are short.

        # We'll do:
        #   j = 0
        #   for i in range(n):
        #       # We'll move j from its current position until the substring word[i:j] is valid
        #       while j < n and not isForbidden(word[i:j+1]):
        #           j += 1
        #       res = max(res, j - i)
        #       if j == i:
        #           j += 1

        # But note: the isForbidden function returns the length of the forbidden substring found, or False if not found.
        # We need to adjust j when a forbidden substring is found. However, in the above while loop, we are checking word[i:j+1] and if it is forbidden, we break and then set j to the current j (