import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    T = sum(A)
    
    # Case 1: Check for multiple full periods
    if s >= T and s % T == 0:
        print("Yes")
        return
        
    # Case 2: Check for contiguous subsequences in two periods (or one period) that sum to s.
    # We'll create a doubled array (two periods) and use prefix sums and a set for the prefix sums of the first period.
    # But note: we are allowed to take any contiguous subsequence (non-empty) in the doubled array (which is of length 2*n) that sums to s.
    # However, we must consider that the contiguous subsequence might be entirely in the first period, or wrap from the first to the second period.

    # We can use a prefix sum array for the doubled array, but note: the doubled array is of length 2*n, which is 400000, which is acceptable.

    # Alternatively, we can use a circular array and two pointers or a sliding window? But note: the array elements are positive (>=1) so we can use two pointers for positive arrays to find a contiguous subsequence with sum s. But wait: the array is positive, so the prefix sum is strictly increasing. However, we are allowed to take any contiguous subsequence (any length). 

    # But note: the problem says the array elements are at least 1, so the array is positive. Therefore, we can use a two-pointer (sliding window) to find a contiguous subsequence that sums to s in the doubled array (if s is less than T, then the contiguous subsequence must be contained in one period or two periods? Actually, if s is less than T, then the contiguous subsequence cannot be more than two periods? Actually, no: because the minimal element is 1, the contiguous subsequence of length L has sum at least L. But we are only concerned with s.

    # However, note: the doubled array is two periods. The maximum contiguous subsequence we need to consider is two periods (because if s >= T, we already handled the multiple full periods). But wait: what if s is between T and 2*T? Then we cannot have a contiguous subsequence that is a multiple of T (because the next multiple is 2*T, and s is less than 2*T). But note: s might be less than T (then we consider one or two periods) or between T and 2*T (then we consider two periods). 

    # Actually, we already handled the case when s is a multiple of T and s>=T. But note: if s is between T and 2*T, then it is not a multiple of T (unless s==k*T for k>=2, but then s>=2*T). So we only handled the case when s is exactly a multiple of T and s>=T.

    # Now, for s < T or T <= s < 2*T (but note: if s>=T and not a multiple, then we don't handle by the multiple case) we need to check in the doubled array.

    # But note: the doubled array is two periods. The contiguous subsequence we are looking for must be contained in two periods (because if it were three periods, then its sum would be at least 3*T, which is >=3*T, and if s < 2*T then we don't need to consider three periods). Actually, the maximum contiguous subsequence we need to consider is two periods (because the minimal element is 1, so the maximum length we need is s (if s is the sum) but note: the array elements are positive, so the contiguous subsequence must be of length at most s (since each element is at least 1). But s can be up to 10^18, so we cannot iterate over each element.

    # We must use a different approach for the case when s < T or T <= s < 2*T (but note: if s>=T and not a multiple, then we are in the two-period case). 

    # Actually, we can combine: we are going to check for any contiguous subsequence (non-empty) in the doubled array (two periods) that sums to s. But note: the doubled array has length 2*n, and n can be up to 200000, so 400000 elements. We can use a prefix sum array and then use a set to record the prefix sums we have seen. But note: the array is positive, so the prefix sums are strictly increasing. We can do:

    # Let B = A + A