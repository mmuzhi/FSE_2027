from typing import List

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        result = []
        for num in nums1:
            idx = nums2.index(num)
            found = False
            for j in range(idx + 1, len(nums2)):
                if nums2[j] > num:
                    result.append(nums2[j])
                    found = True
                    break
            if not found:
                result.append(-1)
        return result