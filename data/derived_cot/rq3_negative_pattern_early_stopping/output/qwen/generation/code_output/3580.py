class Solution:
    def minStartingIndex(self, s: str, pattern: str) -> int:
        n = len(s)
        m = len(pattern)
        # If pattern is empty, then we can consider any substring of length 0, but problem states non-empty substring, so we'll handle accordingly.
        # We'll use a sliding window approach over s of length m.
        # We need to count the number of mismatches between the substring and pattern.
        # But doing a naive O(n*m) would be too slow for n and m up to 10^5.
        # Instead, we can precompute a mismatch array or use a rolling hash? But the problem is about counting mismatches, not exact matching.
        # Alternatively, we can use a two-pointer approach with a fixed window size (m) and keep track of the number of mismatches as we slide the window.
        # Steps:
        # 1. Initialize a variable to keep track of the minimum starting index (or the first index where condition is met).
        # 2. Use a sliding window of length m over s.
        # 3. For each window, count the number of positions where the substring (from s) and pattern differ.
        # 4. If the count is <= 1, then we found a candidate starting index (i.e., the current start index of the window).
        # 5. We need the smallest starting index, so we can return the first candidate we find as we slide from left to right.
        # However, worst-case, if we do a naive count for each window, it's O(n*m) which is 10^10 operations, which is too slow in Python.

        # We need an efficient way to update the mismatch count when moving the window.
        # Idea: Precompute a difference array for the entire string s for the pattern? Or use a rolling hash to quickly compute the number of mismatches? But the problem is about exact matching with at most one change.

        # Alternatively, we can precompute the longest common extension or use a two-pointer with dynamic programming? But that might be overkill.

        # Another idea: Use a fixed-length array and a sliding window with a fixed length (m). We can precompute the first window (from 0 to m-1) and then slide the window one by one, updating the mismatch count by removing the leftmost character and adding the new rightmost character.

        # Steps for efficient approach:
        # 1. Let n = len(s), m = len(pattern)
        # 2. Initialize an array `mismatch` of length n, but actually we can compute on the fly.
        # 3. For the initial window [0, m-1], count the mismatches between s[0:m] and pattern.
        # 4. Then, for each subsequent window starting at i (from 1 to n-m), update the mismatch count:
        #    - Remove the character at i-1: if s[i-1] was equal to pattern[i-1], then we had one less mismatch, but actually, we are moving the window, so we are removing the leftmost character of the previous window and adding a new rightmost character.
        #    Actually, the window moves from [i-1, i-1+m-1] to [i, i+m-1]. So, we remove s[i-1] and add s[i+m-1].
        #    But note: the pattern doesn't move, so the positions in the pattern for the window [i, i+m-1] are still pattern[0:m].
        #    So, when we remove s[i-1], we check if s[i-1] was equal to pattern[i-1]. If it was, then we had one less mismatch (so mismatch_count decreases by 1). Similarly, when we add s[i+m-1], we check if s[i+m-1] is equal to pattern[m-1]. If not, then we have one more mismatch (so mismatch_count increases by 1).
        # 5. But wait, the pattern is fixed, and the window is moving. The pattern's relative position in the window is fixed. So, for the window starting at i, the substring is s[i:i+m]. We compare s[i+j] with pattern[j] for j from 0 to m-1.

        # Actually, the mismatch count for the window starting at i is the number of j in [0, m-1] such that s[i+j] != pattern[j].

        # We can precompute the initial window (i=0) and then update for each i from 1 to n-m.

        # However, updating the entire window for each i would still be O(m) per window, leading to O(n*m) worst-case.

        # We need a way to update the mismatch count