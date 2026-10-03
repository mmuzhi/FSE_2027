import collections
from typing import List

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []
        wlen = len(words[0])
        slen = wlen * len(words)
        n = len(s)
        if n < slen:
            return []
        occ = collections.Counter(words)
        
        def test():
            if len(track) != len(occ):
                return False
            for key in occ:
                if track.get(key, 0) != occ[key]:
                    return False
            return True
        
        res = []
        # If there's only one word, then we can use the above method.
        # For each starting offset k in [0, wlen-1]
        for k in range(wlen):
            track = collections.Counter()
            # Build the frequency dictionary for the window starting at k
            for i in range(k, k+slen, wlen):
                word = s[i:i+wlen]
                if word in occ:
                    track[word] += 1
            if test():
                res.append(k)
            # Now, slide the window by one word at a time
            # The next window starts at k + wlen, then k + 2*wlen, etc.
            # But note: the window length is fixed, so we remove the first word and add the last word.
            # However, the window is built by words, so the first word is at k, and the last word is at k+slen-wlen.
            # But the next window will start at k + wlen, so the first word of the next window is at k+wlen.
            # We can slide the window from k+wlen to the end.
            # But the window must be within the string.
            start_index = k + wlen
            # We'll use a while loop to slide the window
            while start_index + slen <= n:
                # Remove the word that is leaving: the word at start_index - wlen
                word_to_remove = s[start_index - wlen:start_index]
                if word_to_remove in occ:
                    track[word_to_remove] -= 1
                
                # Add the word that is entering: the word at start_index + slen - wlen
                word_to_add = s[start_index + slen - wlen:start_index + slen]
                if word_to_add in occ:
                    track[word_to_add] += 1
                
                if test():
                    res.append(start_index)
                
                start_index += wlen
        
        return res