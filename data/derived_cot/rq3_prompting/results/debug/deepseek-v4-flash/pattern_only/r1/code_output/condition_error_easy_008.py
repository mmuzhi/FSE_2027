from typing import List

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        out = []
        for num in nums1:
            idx = nums2.index(num)
            j = idx + 1
            while j < len(nums2):
                if num < nums2[j]:
                    out.append(nums2[j])
                    break
                j += 1
            else:
                out.append(-1)
        return out