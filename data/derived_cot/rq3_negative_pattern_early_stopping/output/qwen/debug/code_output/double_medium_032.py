class Solution:
    def platesBetweenCandles(self, s: str, queries: List[List[int]]) -> List[int]:
        candies = [i for i, c in enumerate(s) if c == '|']
        
        def bns(x: int) -> int:
            l, r = 0, len(candies) - 1
            while l <= r:
                m = (l + r) // 2
                if candies[m] < x:
                    l = m + 1
                else:
                    r = m - 1
            return l
        
        ans = []
        for a, b in queries:
            l_idx = bns(a)
            r_idx = bns(b + 1) - 1
            if l_idx < r_idx:
                plates = candies[r_idx] - candies[l_idx] - (r_idx - l_idx)
                ans.append(plates)
            else:
                ans.append(0)
        return ans