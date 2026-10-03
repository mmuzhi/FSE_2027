import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    B = list(map(int, data[2:2+n]))
    W = list(map(int, data[2+n:2+n+m]))
    
    # Sort both arrays in descending order
    B.sort(reverse=True)
    W.sort(reverse=True)
    
    # Precompute prefix sums for black and white
    prefixB = [0]*(n+1)
    for i in range(1, n+1):
        prefixB[i] = prefixB[i-1] + B[i-1]
        
    prefixW = [0]*(m+1)
    for i in range(1, m+1):
        prefixW[i] = prefixW[i-1] + W[i-1]
        
    # We'll consider the case of choosing no balls (0) and then consider for each possible l (number of white balls chosen) from 0 to m, and then k from l to n.
    # But that's O(n*m) which is too slow.
    # Instead, we can consider that for a fixed l (number of white balls chosen), we must choose at least l black balls. Then the total sum is prefixB[k] + prefixW[l] for k from l to n.
    # But we need the maximum over k from l to n for each l, and then take the maximum over l from 0 to m.
    # However, note that we can also choose more than l black balls. But the condition is k>=l, so we can choose any k from l to n.

    # But note: the prefixB array is for the best k black balls (since we sorted in descending order). Similarly for white.

    # Now, for each l (from 0 to m), we want to consider the best k (from l to n) and take the maximum prefixB[k] (for k from l to n) and then add prefixW[l]. Then take the maximum over l.

    # But note: the condition is k>=l, so for a fixed l, we can choose any k from l to n. We want the maximum prefixB[k] for k in [l, n]. Then the candidate is max_prefixB_from_l_to_n + prefixW[l].

    # We can precompute an array for the maximum prefixB from index l to n. But note: our prefixB is for the first k elements (the best k). So for k from 0 to n, prefixB[k] is the sum of the top k black balls.

    # Actually, since the black balls are sorted in descending order, prefixB is increasing (if all positive) but not necessarily because there can be negatives. But we want the maximum sum for k black balls, but note: we are allowed to choose any subset of black balls, but the best way is to take the top k (largest values) because if we have negatives, we might not want to take them. But wait, the condition is just the count, so we can choose any subset. However, to maximize the sum, we would always choose the largest values. So the best k black balls are the top k.

    # But note: the condition is that we must choose at least l black balls. So for a fixed l, we can choose any k from l to n. The best sum for black is the maximum of prefixB[k] for k from l to n? Actually, no: because prefixB is the cumulative sum of the sorted (descending) black balls. So prefixB[k] is the sum of the top k black balls. But if we choose more than l black balls, we are adding more balls. But if the additional balls are negative, then the sum might decrease. So actually, for a fixed l, the best black sum is the maximum of prefixB[k] for k from l to n? But note: we are allowed to choose any subset of black balls (not necessarily contiguous in the sorted order) but the best subset of size k is the top k. However, we are forced to choose at least l black balls. So we can choose exactly k black balls (for k from l to n) and we want the maximum sum. But note: the top k black balls might not be the best if we are allowed to choose any subset? Actually, no: because the balls are independent, the best way to choose k black balls is to take the k largest. So the prefixB array is correct.

    # However, note: the condition is that we choose at least l black balls. So we can choose more than l. But the sum of the top k black balls (for k>=l) might be maximized at some k between l and n. But we are allowed to choose