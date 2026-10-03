class Solution:
    def validSubstringCount(self, word1: str, word2: str) -> int:
        n = len(word2)
        if n == 0:
            return 0
        
        # If word2 has duplicate characters, we need to account for that.
        # We'll use two pointers and a sliding window to count the valid substrings.
        # But note: the condition is that the substring must have at least the frequency of each character in word2.
        # We can use a two-pointer approach to expand and contract the window, but we need to count all substrings that satisfy the condition.

        # Alternatively, we can use a two-pointer method to count the number of substrings ending at each index that have at least the frequency of word2.

        # Let's define:
        #   freq2 = frequency map of word2
        #   We'll maintain a window [l, r] and a frequency map for the current window.
        #   We want to count the number of substrings ending at r that have at least the frequency of word2.

        # However, note: the condition is that the substring must have at least the frequency of word2. 
        # But the substring can be of any length (at least n). 

        # We can use a two-pointer approach that expands r and then moves l until the condition is no longer satisfied? 
        # Actually, we want to count all substrings that have the condition. 

        # Another idea: 
        #   We can iterate over the starting index of the substring and then use a pointer to find the minimal length required (which is n) such that the substring from start to that pointer has at least the frequency of word2. Then, all substrings starting at start and ending at any index from that pointer to the end are valid.

        # But that would be O(n^2) which is too slow for n up to 10^5.

        # We need an efficient method.

        # Let's use a two-pointer method to maintain the window [l, r] and a frequency map for the current window. 
        # We'll also keep track of how many characters in the window have frequency >= their frequency in word2 (call it matched). 
        # But note: the condition is that the window must have at least the frequency of word2 for every character. 

        # Actually, we can use a method similar to "count subarrays with at least min frequency" but for multiple characters.

        # Steps:
        #   Let freq2 be the frequency of each character in word2.
        #   Let window_freq be an array (or dictionary) of size 26 (for 'a' to 'z') initialized to 0.
        #   Let matched = 0 (number of distinct characters in word2 that are satisfied in the current window)
        #   Let l = 0, and then iterate r from 0 to len(word1)-1.
        #   For each r, update window_freq for word1[r] and if window_freq[char] becomes >= freq2[char] (and if it was not satisfied before) then increment matched.
        #   Then, while the window [l, r] has matched == len(freq2) (i.e., all characters in word2 are present in sufficient amounts) then we can move l and update matched, but actually we want to count the number of substrings ending at r that are valid.

        # Actually, we want to count all substrings ending at r that are valid. 
        # But note: the condition is that the substring must have at least the frequency of word2. 
        # We can use a two-pointer to find the minimal starting index for each r such that the substring [start, r] is valid. Then, the number of valid substrings ending at r is (r - start + 1) but wait, no: the minimal start index is the one that just satisfies the condition, then any substring starting from 0 to start-1 and ending at r is also valid? Actually, no: the condition is "at least", so if a substring [l, r] is valid, then any substring [l', r] with l' <= l is also valid? Not necessarily: because the condition is about having at least the frequency. But if [l, r] has the frequency, then [l-1, r] might have even more, so it is also valid. 

        # Actually, the condition is monotonic: if a substring [l, r] has at least the frequency of word2, then any substring [l', r] with l' <= l also has at least the frequency (because it includes all the characters from l to l'-1). 

        # So for each r, we can find the smallest l (let's call it left_bound) such that the substring [left_bound