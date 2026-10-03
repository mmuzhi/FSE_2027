class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        out = []
        for num in nums1:
            idx = nums2.index(num)
            j = idx + 1
            found = -1
            while j < len(nums2):
                if num < nums2[j]:
                    found = nums2[j]
                    break
                j += 1
            out.append(found)
        return out