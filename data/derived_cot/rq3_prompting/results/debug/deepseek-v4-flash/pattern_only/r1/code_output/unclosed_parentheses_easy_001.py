import heapq

class Solution:
    def largestInteger(self, num: int) -> int:
        evenlist = []
        oddlist = []
        nums = [int(x) for x in str(num)]

        for digit in nums:
            if digit % 2 == 0:
                evenlist.append(digit)
            else:
                oddlist.append(digit)

        even_heap = [-x for x in evenlist]
        odd_heap = [-x for x in oddlist]
        heapq.heapify(even_heap)
        heapq.heapify(odd_heap)

        result = []
        for digit in nums:
            if digit % 2 == 0:
                result.append(-heapq.heappop(even_heap))
            else:
                result.append(-heapq.heappop(odd_heap))

        return int(''.join(str(x) for x in result))