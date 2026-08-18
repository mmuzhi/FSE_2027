class Solution:
  def arrayChange(self, nums: List[int], operations: List[List[int]]) -> List[int]:
    index_map = {}
    for i, n in enumerate(nums):
      index_map[n] = i
    
    for op in operations:
      n1, n2 = op
      i = index_map[n1]
      nums[i] = n2
      index_map[n2] = i
      del index_map[n1]
    
    return nums