from collections import Counter, defaultdict

class Solution:
    def minimumTotalCost(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        z1 = Counter(nums1)
        z2 = Counter(nums2)
        fixed = defaultdict(list)
        ans = 0
        vis = [0] * n
        
        for i in range(n):
            if nums1[i] == nums2[i]:
                ans += 2 * i
                fixed[nums1[i]].append(i)
                vis[i] = 1
        
        freq = Counter()
        for num in fixed:
            freq[num] += len(fixed[num])
        
        if not freq:
            return ans
        
        most_common = freq.most_common(1)[0][0]
        count_fixed = freq[most_common]
        remaining = n - sum(vis)
        
        if count_fixed >= (remaining + 1) // 2:
            return ans
        
        for i in range(n):
            if not vis[i]:
                if nums1[i] == most_common or nums2[i] == most_common:
                    ans += i
                    vis[i] = 1
        
        return ans