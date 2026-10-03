class Solution:
    def sortString(self, s: str) -> str:
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1
        
        letters = sorted(freq.keys())
        left = 0
        right = len(letters) - 1
        res = []
        
        while left <= right:
            # Move left pointer until a letter with positive frequency is found
            while left <= right and freq[letters[left]] == 0:
                left += 1
            if left > right:
                break
            res.append(letters[left])
            freq[letters[left]] -= 1
            if freq[letters[left]] == 0:
                left += 1
            
            # Move right pointer until a letter with positive frequency is found
            while left <= right and freq[letters[right]] == 0:
                right -= 1
            if left > right:
                break
            res.append(letters[right])
            freq[letters[right]] -= 1
            if freq[letters[right]] == 0:
                right -= 1
        
        return ''.join(res)