class Solution:
    def longestPalindrome(self, s: str, t: str) -> int:
        max_len = 0
        n = len(s)
        m = len(t)
        # Iterate over all substrings of s
        for i in range(n + 1):
            for j in range(i, n + 1):
                A = s[i:j]
                # Iterate over all substrings of t
                for k in range(m + 1):
                    for l in range(k, m + 1):
                        B = t[k:l]
                        candidate = A + B
                        # Check if candidate is palindrome
                        if candidate == candidate[::-1]:
                            if len(candidate) > max_len:
                                max_len = len(candidate)
        return max_len