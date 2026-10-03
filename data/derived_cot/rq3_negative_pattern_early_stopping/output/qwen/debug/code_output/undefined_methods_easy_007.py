class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        l = []
        for i in nums1:
            try:
                idx = nums2.index(i)
            except ValueError:
                l.append(-1)
                continue
            found = False
            for k in range(idx + 1, len(nums2)):
                if nums2[k] > i:
                    l.append(nums2[k])
                    found = True
                    break
            if not found:
                l.append(-1)
        return l