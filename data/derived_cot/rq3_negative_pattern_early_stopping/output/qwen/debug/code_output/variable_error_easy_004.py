class Solution:
    def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        nums, sums, res, n = sorted(nums), [0], [], len(queries)+1
        for num in nums:
            sums.append(sums[-1] + num)
        
        # Change n to be the length of the prefix sum array (which is len(nums)+1)
        n = len(sums)
        def bSearch(q, l=0, mid=n>>1, r=n):
            while l < mid < r:
                if sums[mid] > q:
                    r = mid
                elif sums[mid] < q:
                    l = mid + 1
                else:
                    break
                mid = (l + r) >> 1
            return mid
        
        return [bSearch(q) for q in queries]