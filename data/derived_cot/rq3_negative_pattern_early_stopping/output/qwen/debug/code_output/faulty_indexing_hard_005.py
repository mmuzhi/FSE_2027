class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not words:
            return []
        wlen = len(words[0])
        n = len(s)
        word_count = len(words)
        total_len = wlen * word_count
        occ = collections.Counter(words)
        res = []
        
        # If the total length is more than the string, return empty list
        if n < total_len:
            return res
        
        # We'll use a sliding window that moves by wlen each time
        # For each starting offset k in [0, wlen-1]
        for k in range(wlen):
            # Build frequency dictionary for the first window
            freq = {}
            # Check if the first window is valid
            start = k
            # We'll break the first window into words
            valid = True
            # First, check if the substring from start to start+total_len is available
            if start + total_len > n:
                continue
            # Build the frequency dictionary for the first window
            for i in range(word_count):
                word = s[start + i*wlen: start + (i+1)*wlen]
                freq[word] = freq.get(word, 0) + 1
            # Check if the first window matches
            if freq == occ:
                res.append(start)
            # Slide the window
            # The next window starts at start + wlen, then start + 2*wlen, etc.
            # We'll slide until the window goes beyond the string
            # The current window is from start to start+total_len-1
            # The next window is from start+wlen to start+wlen+total_len-1
            # We remove the word at start and add the word at start+total_len (if available)
            # But note: the window is of fixed length total_len, so we remove the first word and add the next word.
            # However, the windows are not overlapping, so we cannot update by removing one word and adding one word.
            # Instead, we need to recompute the frequency dictionary for the new window.
            # But note: the new window is the old window without the first word and with the next word? Actually, no: the windows are adjacent and non-overlapping.
            # So we cannot update by removing one word and adding one word because the windows are not overlapping.
            # Therefore, we must recompute the frequency dictionary for each window.
            # But that would be O(n) per window, which is acceptable if the number of windows is small.
            # However, we can update by removing the first word of the current window and adding the next word (if the window moves by one word, but note: the window moves by wlen, so we remove one word and add one word).
            # But wait, the window moves by wlen, so we remove the word at start and add the word at start+total_len (if start+total_len < n).
            # However, the window is of length total_len, so the next window is the current window without the first word and with the next word? Actually, the next window is the current window without the first word and with the next word, but the next word is at start+total_len (which is the next word after the current window).
            # But note: the current window is from start to start+total_len-1. The next window is from start+wlen to start+wlen+total_len-1. The two windows are adjacent, so the next window does not contain the first word of the current window. Therefore, we cannot update by removing the first word.
            # We must recompute the frequency dictionary for each window.
            # But note: the problem constraints might be large, so we need an efficient way.
            # Alternatively, we can update the frequency dictionary by removing the first word and adding the next word, but note that the windows are not overlapping. So the next window is completely different.
            # Therefore, we must recompute the frequency dictionary for each window.
            # However, we can do it by breaking the window into words.
            # But note: the window is of fixed length total_len, so we can break it into word_count words.
            # We'll do:
            #   For each window starting at i (which is k + t*wlen), we break the substring s[i:i+total_len] into words and update the frequency dictionary.
            # But that would be O(n) per window, and the number of windows is (n - total_len) / wlen, which might be too slow.
            # We need to optimize.
            # Let's change the approach: we'll use a fixed window of length total_len and slide by wlen. We'll break the window into words and update the frequency dictionary by removing the first word