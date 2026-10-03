class Solution:
    def findTheString(self, lcp: List[List[int]]) -> str:
        n = len(lcp)
        # Check symmetry and bounds for i < j
        for i in range(n):
            for j in range(i + 1, n):
                if lcp[i][j] != lcp[j][i]:
                    return ''
                if lcp[i][j] > n - j:
                    return ''
        # Check diagonal
        for i in range(n):
            if lcp[i][i] != n - i:
                return ''
        
        # Build pattern array
        pattern = [None] * n
        next_el_ind = 0
        for i in range(n):
            if pattern[i] is not None:
                continue
            pattern[i] = next_el_ind
            next_el_ind += 1
            for j in range(i+1, n):
                if lcp[i][j] > 0:
                    if pattern[j] is not None and pattern[j] != pattern[i]:
                        return ''
                    pattern[j] = pattern[i]
        
        # Build pattern LCP matrix from pattern
        pattern_lcp = [[0] * n for _ in range(n)]
        for i in range(n-1, -1, -1):
            for j in range(n-1, -1, -1):
                if pattern[i] == pattern[j]:
                    if max(i, j) + 1 < n:
                        pattern_lcp[i][j] = pattern_lcp[i+1][j+1] + 1
                    else:
                        pattern_lcp[i][j] = 1
                else:
                    pattern_lcp[i][j] = 0
        
        # Compare with original LCP
        for i in range(n):
            for j in range(n):
                if lcp[i][j] != pattern_lcp[i][j]:
                    return ''
        
        # Check that the pattern has at most 26 distinct characters
        if max(pattern) >= 26:
            return ''
        
        return ''.join(chr(ord('a') + x) for x in pattern)
