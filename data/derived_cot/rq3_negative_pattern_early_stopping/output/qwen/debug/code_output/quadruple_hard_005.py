class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        p1 = 0
        p2 = 0
        merged = []
        
        while p1 < len(nums1) and p2 < len(nums2):
            if nums1[p1] < nums2[p2]:
                merged.append(nums1[p1])
                p1 += 1
            else:
                merged.append(nums2[p2])
                p2 += 1
        
        while p1 < len(nums1):
            merged.append(nums1[p1])
            p1 += 1
        
        while p2 < len(nums2):
            merged.append(nums2[p2])
            p2 += 1
        
        total_length = len(merged)
        if total_length % 2 == 1:
            return float(merged[total_length // 2])
        else:
            return (merged[total_length // 2 - 1] + merged[total_length // 2]) / 2.0