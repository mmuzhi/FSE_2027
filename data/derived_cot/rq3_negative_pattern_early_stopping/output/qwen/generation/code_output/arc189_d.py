import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # We'll do two passes: one from left to right and one from right to left.
    # We want for each index i, the maximum value we can get.

    # Let L[i] be the maximum value we can get from the left side (including the starting point) if we only merge to the left.
    # But note: we can merge both left and right arbitrarily. However, the merging of left and right is independent in the sense that we can merge all the strictly smaller slimes to the left and all the strictly smaller slimes to the right, but the condition for merging a slime depends on the current value.

    # Alternate approach: 
    #   We can precompute two arrays:
    #   left_max[i]: the maximum value we can get from the contiguous segment to the left (including the starting point) without being blocked by a slime that is too large (but note: we can merge even if we become larger than a previously encountered larger slime? Actually, we can merge a slime only if it is strictly smaller than the current value, and the current value increases as we merge.

    # However, note: the problem is similar to the "expanding" of the starting slime by merging all the strictly smaller slimes that are connected (left and right) but the condition for merging a slime is that it is strictly smaller than the current value.

    # We can use a stack-based method or dynamic programming.

    # Insight: 
    #   We can only merge a slime if it is strictly smaller than the current value. And the current value is the starting value plus the sum of all the absorbed slimes (which are strictly smaller). 

    # But note: the order of merging does not matter for the total sum? Actually, the total sum is the sum of all the strictly smaller slimes that are connected (left and right) and that are not blocked by a larger slime that we cannot merge. However, we can merge a larger slime if we have become large enough by merging smaller ones.

    # Actually, the problem is equivalent to: 
    #   We can merge all the slimes that are strictly smaller than the maximum value we can achieve. But the maximum value we can achieve is the starting value plus the sum of all the strictly smaller slimes that are connected (left and right) and that are not separated by a slime that is >= the starting value? 

    # Let's reframe: 
    #   We can only merge a slime if it is strictly smaller than the current value. But the current value is the starting value plus the sum of the absorbed slimes. 

    # However, note: we can merge a slime that is smaller than the starting value, then the current value increases, and then we can merge a slime that is smaller than the new current value (which might be larger than the starting value). 

    # Therefore, the total sum we can get is the sum of all the slimes that are strictly smaller than the maximum value we can achieve. But that is circular.

    # Another idea: 
    #   We can use a two-pass method (like the "largest rectangle in histogram" or "next greater element") to determine the boundaries (the nearest larger slime to the left and right). Then, within the boundaries, we can merge all the strictly smaller slimes.

    # But note: even if there is a larger slime, if we merge enough smaller ones to become larger than that larger slime, we can merge it. So the boundary is not a fixed larger slime, but the condition is: we can merge a slime if it is strictly smaller than the current value, and the current value is the starting value plus the sum of all the strictly smaller slimes we've merged.

    # This seems difficult.

    # Known similar problems: 
    #   "Slime Combining" (but that is a different problem) and "Absorption" problems.

    # Another known idea: 
    #   We can use a stack to compute the next greater or equal element to the left and right. Then, the starting slime can merge all the slimes that are strictly smaller than the starting slime and that are between the boundaries (the next greater or equal element). But wait, what if the starting slime is small and there is a larger slime to the right, but then we merge a lot of small slimes and become larger than that larger slime? Then we can merge beyond the initial boundary.

    # Actually, the boundary is not fixed. We can merge beyond the initial boundary if we become large enough.

    # We need to compute the maximum value we can achieve for each starting point.

    # Let's define:
    #   Let L[i] = the maximum value we can achieve from the left side (from index