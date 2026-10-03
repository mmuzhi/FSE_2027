class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int):
        dico = defaultdict(list)
        for profit, category in items:
            dico[category].append(profit)
        categories = []
        for category in dico:
            categories.append(sorted(dico[category]))
        categories.sort(key=lambda x: x[-1], reverse=True)
        
        def elegance(distinct):
            res = 0
            rest = []
            for i in range(distinct):
                if not categories[i]:
                    return -1
                res += categories[i][-1]
                rest.extend(categories[i][:-1])
            rest.sort(reverse=True)
            if len(rest) < k - distinct:
                return -1
            return res + sum(rest[:k - distinct]) + distinct**2
        
        l, r = 1, min(len(categories), k)
        ans = -1
        while l <= r:
            mid = (l + r) // 2
            val = elegance(mid)
            if val != -1:
                ans = max(ans, val)
                l = mid + 1
            else:
                r = mid - 1
        return ans
