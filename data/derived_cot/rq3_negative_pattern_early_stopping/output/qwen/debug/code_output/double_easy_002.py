import heapq

class Solution:
    def largestInteger(self, num: int) -> int:
        if num == 0:
            return 0
        nums = [int(x) for x in str(num)]
        evenlist = []
        oddlist = []
        for i in nums:
            if i % 2 == 0:
                evenlist.append(i)
            else:
                oddlist.append(i)
        even = [-x for x in evenlist]
        odd = [-x for x in oddlist]
        heapq.heapify(even)
        heapq.heapify(odd)
        result = []
        for ele in nums:
            if ele % 2 == 0:
                result.append(-heapq.heappop(even))
            else:
                result.append(-heapq.heappop(odd))
        result = [str(x) for x in result]
        return int(''.join(result))