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
            for c in s:
                if c not in t:
                    return False
                t = t[c]
                if "end" in t:
                    return True
            return False
        
        res = 0
        j = len(word)
        for i in range(len(word) - 1, -1, -1):
            if isForbidden(word[i:j]):
                # We need to find the minimal forbidden substring starting at i
                # We'll traverse from i until we find the forbidden substring and then set j to the next index after the forbidden substring
                # But note: the helper function doesn't tell us the exact forbidden substring's end, so we can't set j directly.
                # Instead, we can do: we know that the substring starting at i is forbidden, so we set j to i (so that the substring from i to j-1 is empty and valid) but that is too restrictive.
                # Alternatively, we can use a two-pointer approach to find the minimal forbidden substring starting at i and then set j to the end of that substring + 1.
                # However, the current approach is to check from the end and update j. Let's change the approach.

        # Let's change the approach: we'll use a two-pointer (i, j) and move j from 0 to len(word)-1, and maintain a set of forbidden substrings in the current window? 
        # But the problem is that the forbidden substrings can be long and we have many.

        # Alternatively, we can use a sliding window and a trie to check for forbidden substrings. But the original code was trying to do it from the end.

        # Let's fix the original idea: we want to find the longest substring that does not contain any forbidden substring. We can do:

        # We'll traverse from the end and keep track of the last forbidden substring's end. But the helper function `isForbidden` returns True if the substring contains a forbidden substring, but it doesn't tell us the exact forbidden substring's end.

        # Revised plan for the helper function: we want to know the minimal forbidden substring that starts at a given index. But that is expensive.

        # Another idea: we can use a set of forbidden substrings and then use a two-pointer to check for forbidden substrings. But the forbidden list can be long.

        # Alternatively, we can use a rolling hash to check for forbidden substrings, but that might be overkill.

        # Let's stick to the trie and try to fix the helper function to return the end index of the forbidden substring.

        # We can modify the helper function to return the index (within the substring) where the forbidden substring ends, or -1 if not found.

        # Then, in the main loop, if we find a forbidden substring starting at `i` and ending at `i+truc-1` (where `truc` is the length), then we set `j = i+truc` (so that the substring from `i` to `j-1` is forbidden and we cannot extend beyond `j-1`).

        # But note: the substring we are checking is `word[i:j]`. We want to know the minimal forbidden substring starting at `i` and then set `j` to the next index after that forbidden substring.

        # Let's change the helper function to return the index (within the substring) of the end of the forbidden substring, or -1 if not found.

        # However, the problem is that there might be multiple forbidden substrings and we want to avoid any. So we must set `j` to the minimal index such that the substring from `i` to `j-1` is forbidden-free.

        # Actually, we can do: if we find a forbidden substring starting at `i`, then we set `j` to the end of that forbidden substring + 1. But note: there might be a longer forbidden substring that starts earlier? But we are starting at `i`, so we are only concerned with substrings starting at `i`.

        # We can modify the helper function to return the length of the forbidden substring found, but then we must ensure that we are only considering the minimal one? Actually, we want to set `j` to the minimal index that breaks the condition, so we want the minimal forbidden substring starting at `i`.

        # But note: the problem is that the forbidden substring might be a substring of another forbidden substring. However, we are only concerned with the first occurrence of a forbidden substring.