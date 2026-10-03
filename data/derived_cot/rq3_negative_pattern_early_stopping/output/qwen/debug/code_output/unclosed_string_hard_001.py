class Solution:
    def palindromePartition(self, s: str, k: int) -> int:
        def Cost(sub):
            i, j = 0, len(sub) - 1
            changes = 0
            while i < j:
                if sub[i] != sub[j]:
                    changes += 1
                i += 1
                j -= 1
            return changes
        
        dp = {}
        
        def A(sub, k):
            if (sub, k) in dp:
                return dp[(sub, k)]
            
            if k == 1:
                dp[(sub, k)] = Cost(sub)
                return dp[(sub, k)]
            
            min_cost = float('inf')
            n = len(sub)
            for x in range(1, n):
                cost_here = Cost(sub[:x])
                cost_rest = A(sub[x:], k-1)
                if cost_here == -1 or cost_rest == -1:
                    continue
                total_cost = cost_here + cost_rest
                if total_cost < min_cost:
                    min_cost = total_cost
            
            dp[(sub, k)] = min_cost if min_cost != float('inf') else -1
            return dp[(sub, k)]
        
        result = A(s, k)
        return result if result != float('inf') else -1