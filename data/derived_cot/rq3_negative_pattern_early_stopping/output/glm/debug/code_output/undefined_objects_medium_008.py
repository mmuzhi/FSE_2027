from typing import List
from collections import defaultdict

class Solution:
  def arrayChange(self, nums: List[int], operations: List[List[int]]) -> List[int]:
    index_map = defaultdict(int)
    for i, n in enumerate(nums):
      index_map[n] = i
    
    for op in operations:
      n1, n2 = op
      idx = index_map.pop(n1)
      nums[idx] = n2
      index_map[n2] = idx
    
    return nums