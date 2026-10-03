import heapq

class Solution:
    def largestInteger(self, num: int) -> int:
        evenlist = []
        oddlist = []
        nums = [int(x) for x in str(num)]
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
        return int(''.join(map(str, result)))