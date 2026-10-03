class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not words:
            return []
        wlen = len(words[0])
        n = len(s)
        word_count = len(words)
        total_length = word_count * wlen
        
        # If the total length is more than the string, return empty list
        if n < total_length:
            return []
        
        # Frequency dictionary for words
        occ = collections.Counter(words)
        
        # Helper function to check if the current track matches occ
        def check():
            for word, count in occ.items():
                if track[word] != count:
                    return False
            return True
        
        res = []
        # We'll use a sliding window of fixed length total_length
        # We consider starting offsets from 0 to wlen-1
        # For each offset, we'll slide a window of length total_length and update the frequency dictionary
        
        # Initialize the frequency dictionary for the first window for each offset
        # But note: we are going to do for each offset separately
        # We can do: for each offset k, we consider the window starting at k and then slide by wlen each time
        
        # However, we can optimize by reusing the previous window's frequency dictionary
        # But for simplicity, we'll do for each offset separately
        
        # We'll use a dictionary to keep track of the current frequency of words in the window
        # But note: the window is of fixed length total_length, so we break it into word_count words of length wlen
        
        # We'll iterate over each starting offset k from 0 to wlen-1
        for k in range(wlen):
            # Initialize the frequency dictionary for the current offset
            track = {}
            # Build the initial window for offset k
            # The window starts at k and has length total_length
            # We break it into word_count words of length wlen
            # But note: the window might not be fully in the string? We need to check
            if k + total_length > n:
                continue
            # Initialize the frequency dictionary for the first window
            for i in range(word_count):
                start_index = k + i * wlen
                end_index = start_index + wlen
                word = s[start_index:end_index]
                track[word] = track.get(word, 0) + 1
            
            # Check if the initial window matches
            if check():
                res.append(k)
            
            # Now slide the window by one word (wlen) each time
            # The next window starts at k + wlen, then k + 2*wlen, etc.
            # But note: the window must be of length total_length, so the next window starts at k + wlen and ends at k + wlen + total_length - 1
            # We are going to slide until the window is within the string
            # The next window starts at k + wlen, then k + 2*wlen, ... until k + (m-1)*wlen + total_length <= n
            # But note: the window is fixed length, so we are effectively moving the window by one word each time
            # We remove the first word of the previous window and add the next word
            # But note: the window is of fixed length, so we are always looking at a contiguous block of word_count words
            # However, the window moves by one word, so we remove the word at the beginning and add the word at the end
            
            # The current window starts at k + (current_index) * wlen, but we are sliding by one word each time
            # We are going to slide from the initial window (which starts at k) to the next window (which starts at k + wlen) and so on
            # The number of windows for offset k is: (n - total_length + 1 - k) // wlen + 1? Actually, we are moving by wlen each time, so the next window starts at k + wlen, then k + 2*wlen, etc.
            # But note: the window must be of length total_length, so the start index must be <= n - total_length
            # The next window starts at k + wlen, then k + 2*wlen, ... until k + (m-1)*wlen <= n - total_length
            
            # We already did the first window (start at k). Now we slide the window by one word (wlen) each time
            # The next window starts at k + wlen, then k + 2*wlen, etc.
            # We'll iterate from start_index = k + wlen to n - total_length (inclusive) with step wlen
            # But note: the window is of fixed length,