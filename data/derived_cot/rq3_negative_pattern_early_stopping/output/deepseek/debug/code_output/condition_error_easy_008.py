from typing import List

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        out = []
        for num in nums1:
            idx = nums2.index(num)
            j = idx + 1
            found = False
            while j < len(nums2):
                if nums2[j] > num:
                    out.append(nums2[j])
                    found = True
                    break
                j += 1
            if not found:
                out.append(-1)
        return out