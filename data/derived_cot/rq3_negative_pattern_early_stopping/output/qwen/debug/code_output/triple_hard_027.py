class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        p1 = 0
        p2 = 0
        new = []
        while p1 < len(nums1) and p2 < len(nums2):
            if nums1[p1] < nums2[p2]:
                new.append(nums1[p1])
                p1 += 1
            else:
                new.append(nums2[p2])
                p2 += 1
        while p1 < len(nums1):
            new.append(nums1[p1])
            p1 += 1
        while p2 < len(nums2):
            new.append(nums2[p2])
            p2 += 1
        
        n = len(new)
        if n % 2 == 0:
            index = n // 2
            median = (new[index] + new[index - 1]) / 2.0
        else:
            median = float(new[n // 2])
        return median