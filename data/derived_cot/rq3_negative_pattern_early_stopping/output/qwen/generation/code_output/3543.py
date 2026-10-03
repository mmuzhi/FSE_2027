class Solution:
    def countKConstraintSubstrings(self, s: str, k: int) -> int:
        n = len(s)
        total_substrings = n * (n + 1) // 2
        
        # Count substrings with zeros <= k (condition A)
        countA = 0
        zeros = 0
        left = 0
        for right in range(n):
            if s[right] == '0':
                zeros += 1
            while zeros > k and left <= right:
                if s[left] == '0':
                    zeros -= 1
                left += 1
            countA += (right - left + 1)
        
        # Count substrings with ones <= k (condition B)
        countB = 0
        ones = 0
        left = 0
        for right in range(n):
            if s[right] == '1':
                ones += 1
            while ones > k and left <= right:
                if s[left] == '1':
                    ones -= 1
                left += 1
            countB += (right - left + 1)
        
        # Count substrings with both zeros <= k and ones <= k (condition A ∩ B)
        countAB = 0
        zeros = 0
        ones = 0
        left = 0
        for right in range(n):
            if s[right] == '0':
                zeros += 1
            else:
                ones += 1
            while zeros > k or ones > k:
                if s[left] == '0':
                    zeros -= 1
                else:
                    ones -= 1
                left += 1
            countAB += (right - left + 1)
        
        # By inclusion-exclusion: |A ∪ B| = |A| + |B| - |A ∩ B|
        return countA + countB - countAB