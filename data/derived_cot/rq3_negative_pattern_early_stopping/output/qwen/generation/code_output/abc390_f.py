import sys
from collections import defaultdict

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # Precompute next and previous occurrence for each number to help in determining the range of numbers that must be covered.
    # We'll compute for each distinct number the first and last occurrence in the entire array? But we need to consider subarrays.
    # Alternatively, we can use a different approach: think about the necessary condition for an operation to be performed.

    # Insight: The problem is equivalent to covering the distinct numbers in the subarray with intervals. But note: the operation condition requires that the interval [l, r] must contain every number that is present in the current multiset? No, the condition is that every integer from l to r must appear at least once. So if we have a set S of numbers, then we can choose an interval [l, r] that is a subset of S (but not necessarily contiguous in S) but must be contiguous in the number line. Actually, the condition is that [l, r] is a contiguous interval and every integer in [l, r] must be in S. Then, we remove all numbers in [l, r] from S.

    # This is similar to the "minimum number of intervals to cover all points" but here the intervals are fixed (from 1 to N) and we can choose any contiguous interval that is contained in S. But note: we are allowed to choose any contiguous interval [l, r] as long as S contains every integer from l to r. Then, we remove all numbers in [l, r] from S.

    # Actually, the problem is equivalent to: given a set S (the distinct numbers in the subarray), we want to cover S with the minimum number of contiguous intervals (each interval [l, r] must be contained in S, meaning S contains every integer from l to r). But note: we are allowed to cover non-consecutive numbers in one operation if they form a contiguous interval? Actually, no: the operation erases all numbers in [l, r] (even if they are not consecutive in the array, but they must be consecutive in the number line). 

    # However, the catch is that the operation condition requires that the interval [l, r] is contiguous in the number line and that every number in [l, r] is present. Then, we remove all occurrences of those numbers. 

    # But note: the same number might appear multiple times, but that doesn't matter because we remove all occurrences. 

    # Now, the key is: for a given subarray, we have a set S (the distinct numbers). We want to cover S with the minimum number of contiguous intervals (each interval must be a contiguous set of numbers from 1 to N). 

    # However, note that the operations can be done in any order, and the condition for an operation is independent of the order. So the problem reduces to: given a set S (subset of {1,2,...,N}), what is the minimum number of contiguous intervals needed to cover S? 

    # But wait: the condition for an operation is that the interval [l, r] must be contained in S (i.e., S must contain every integer from l to r). Then, we remove [l, r] from S. 

    # This is the same as: we want to cover S with intervals that are contiguous in the number line and that are contained in S. But note: the intervals must be maximal? Actually, no. We can choose any contiguous interval that is contained in S. 

    # Example: S = {1,3,4}. Then we can choose [1,1] and [3,4]. But we cannot choose [1,4] because 2 is missing. So the minimal covering is two intervals.

    # So the problem for a fixed subarray is: given a set S (the distinct numbers in the subarray), what is the minimum number of contiguous intervals (from 1 to N) that are contained in S and that cover S?

    # This is a classic interval covering problem. We can sort S and then merge intervals? Actually, we can think of it as: we want to cover the set S with intervals that are contiguous and contained in S. The minimal number of intervals is the number of "gaps" in S plus one? 

    # Let S be sorted. Then, the minimal covering is achieved by covering each maximal contiguous block in S. For example, if S = {1,2,3,5,6}, then we have two contiguous blocks: [1,3] and [5,6]. So we need two operations.

    # Therefore, for a subarray, let S be the set of distinct numbers. Then, f(L,R