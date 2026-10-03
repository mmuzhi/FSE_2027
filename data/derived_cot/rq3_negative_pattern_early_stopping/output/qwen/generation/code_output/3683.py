class Solution:
    def answerString(self, word: str, numFriends: int) -> str:
        n = len(word)
        required = numFriends - 1
        # If numFriends is 1, then the only valid substring is the entire word.
        if numFriends == 1:
            return word
        
        # We'll iterate over all substrings
        best = ""
        # Iterate over start index i
        for i in range(n):
            # Iterate over end index j from i to n-1
            for j in range(i, n):
                # Calculate left and right lengths
                left = i  # prefix length
                right = n - j - 1  # suffix length
                # The substring is word[i:j+1]
                # Check if this substring is a valid part
                if left == 0 and right == 0:
                    # This is the entire word, valid only if required==0 (numFriends==1)
                    if required == 0:
                        candidate = word[i:j+1]
                        if candidate > best:
                            best = candidate
                elif left == 0:
                    # Only right part exists
                    if required >= 1 and required <= right:
                        candidate = word[i:j+1]
                        if candidate > best:
                            best = candidate
                elif right == 0:
                    # Only left part exists
                    if required >= 1 and required <= left:
                        candidate = word[i:j+1]
                        if candidate > best:
                            best = candidate
                else:
                    # Both left and right exist
                    k_min = max(1, required - right)
                    k_max = min(left, required - 1)
                    if k_min <= k_max:
                        candidate = word[i:j+1]
                        if candidate > best:
                            best = candidate
        return best