class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []
        wlen = len(words[0])
        n = len(s)
        word_count = len(words)
        total_len = word_count * wlen
        
        # If the total length is larger than s, return empty list
        if total_len > n:
            return []
        
        # Build frequency map for words
        occ = collections.Counter(words)
        
        # For each starting offset k in [0, wlen)
        res = []
        for k in range(wlen):
            # Initialize current frequency map
            cur_count = {}
            # Initialize the window from k to k+total_len
            # But we need to check the first window of length total_len starting at k
            start = k
            end = start + total_len
            # If the window exceeds the string, skip
            if end > n:
                continue
            # Count words in the first window
            for j in range(start, end, wlen):
                word = s[j:j+wlen]
                cur_count[word] = cur_count.get(word, 0) + 1
            
            # Check if the current window matches
            if self.match(occ, cur_count):
                res.append(start)
            
            # Slide the window
            # We'll slide from start + wlen to n - total_len + wlen
            for i in range(start + wlen, n - total_len + 1, wlen):
                # Remove the word that is leaving the window (at the beginning of the window)
                left_word = s[i - total_len:i - total_len + wlen]
                cur_count[left_word] -= 1
                if cur_count[left_word] == 0:
                    del cur_count[left_word]
                
                # Add the new word that is entering the window (at the end of the window)
                right_word = s[i:i+wlen]
                cur_count[right_word] = cur_count.get(right_word, 0) + 1
                
                if self.match(occ, cur_count):
                    res.append(i)
        return res

    def match(self, occ, cur_count):
        # Check if cur_count matches occ
        for word, count in occ.items():
            if word not in cur_count or cur_count[word] != count:
                return False
        return True
