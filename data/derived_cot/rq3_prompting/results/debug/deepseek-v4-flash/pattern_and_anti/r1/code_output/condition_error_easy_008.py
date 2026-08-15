from typing import List

class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        out = []
        for i in range(len(nums1)):
            idx = nums2.index(nums1[i])
            if idx == len(nums2) - 1:
                out.append(-1)
            else:
                j = idx + 1
                while j < len(nums2):
                    if nums1[i] < nums2[j]:
                        out.append(nums2[j])
                        break
                    j += 1
                else:
                    out.append(-1)
        return out