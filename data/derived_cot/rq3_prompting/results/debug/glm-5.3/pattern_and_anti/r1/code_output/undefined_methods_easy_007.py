class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        l = []
        for i in nums1:
            count = 0
            for idx, j in enumerate(nums2):
                if i == j:
                    for k in range(idx + 1, len(nums2)):
                        if nums2[k] > j:
                            count += 1
                            l.append(nums2[k])
                            break
                    if count == 0:
                        l.append(-1)
                    break
        return l