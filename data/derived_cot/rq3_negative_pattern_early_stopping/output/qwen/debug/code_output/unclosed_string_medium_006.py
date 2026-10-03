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
            l_index = bns(a)
            r_index = bns(b + 1) - 1
            if l_index < r_index:
                ans.append(candies[r_index] - candies[l_index] - (r_index - l_index))
            else:
                ans.append(0)
        return ans
