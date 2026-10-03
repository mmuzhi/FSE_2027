class Solution:
    def maxRemovals(self, source: str, pattern: str, targetIndices: List[int]) -> int:
        n = len(source)
        m = len(pattern)
        # If pattern is empty, we can remove all targetIndices
        if m == 0:
            return len(targetIndices)
        
        # We'll use two pointers for the pattern and source
        j = 0  # pointer for pattern
        removals = 0  # count of removals we can do
        # We'll iterate over the source
        for i in range(n):
            # If we have matched the entire pattern, we can break
            if j == m:
                break
            # If the current character matches the pattern character, then we can consider skipping (removing) this character if it is in targetIndices and there is an alternative