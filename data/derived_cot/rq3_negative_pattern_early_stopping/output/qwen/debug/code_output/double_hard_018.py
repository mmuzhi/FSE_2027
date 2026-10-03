class Solution:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        bl = [False] * n
        mx = -1
        
        for i in range(n):
            if not bl[i]:
                x = i
                l = 0
                st = set()
                while x != -1 and not bl[x]:
                    bl[x] = True
                    st.add(x)
                    l += 1
                    x = edges[x]
                if x != -1 and x in st:
                    cycle_length = l - st.index(x) - 1
                    if cycle_length > mx:
                        mx = cycle_length
        return mx