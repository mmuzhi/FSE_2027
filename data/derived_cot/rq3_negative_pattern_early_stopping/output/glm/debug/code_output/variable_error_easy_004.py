class Solution:
  def answerQueries(self, nums: List[int], queries: List[int]) -> List[int]:
    nums.sort()
    sums = [0]
    for num in nums:
      sums.append(sums[-1] + num)
    n = len(sums)
    
    def bSearch(q):
      l, r = 0, n
      while l < r:
        mid = (l + r) >> 1
        if sums[mid] > q:
          r = mid
        else:
          l = mid + 1
      return l - 1

    return [bSearch(q) for q in queries]