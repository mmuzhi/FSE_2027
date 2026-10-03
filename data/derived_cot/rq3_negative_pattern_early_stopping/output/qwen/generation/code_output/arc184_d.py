def main():
    import sys
    data = sys.stdin.read().strip().split()
    n = int(data[0])
    points = []
    index = 1
    for i in range(n):
        x = int(data[index]); y = int(data[index+1]); index += 2
        points.append((x, y))
    
    # Sort the points by x-coordinate (and then by y-coordinate for stability)
    points.sort(key=lambda p: (p[0], p[1]))
    
    # Build a 2D DP table for longest increasing subsequence (LIS) type but for dominance?
    # Alternatively, use dynamic programming with state as the last point and then use a Fenwick tree or segment tree for counting.
    # But note: the problem is about counting the number of sets that are "independent" in the dominance graph.

    # Actually, the problem is equivalent to counting the number of antichains in the poset defined by the dominance relation (Pareto dominance) but with strict inequalities.

    # However, note the constraints: N up to 300. So, we can use an O(N^2) or O(N^3) solution.

    # Another idea: the set S is valid if and only if for any two points in S, neither dominates the other (i.e., S is an antichain). But wait, in the sample, {1,2} is valid and {1,3} is valid, and {1,2,3} is valid. But {2,3} is not valid. Why? Because if we have {2,3}, then we can remove 2 by choosing 3? But wait, the operation condition for removing 2: we need a ball that is greater than 2 in both coordinates. 3 is (3,2) and 2 is (2,1). So 3 has x=3>2 and y=2>1, so yes, 3 dominates 2. So if 3 is present, we can remove 2. But wait, the set {2,3} is not allowed because we can remove 2 without removing 3? Actually, the problem states that the set remaining is the set that is never removed. So if we have {2,3}, then we must have not removed 2 and 3. But to have {2,3} remaining, we must not have chosen any operation that removes 2 or 3. 

    # But note: the operation can be performed any number of times. So, if we choose 3, we remove 2. Therefore, if we want {2,3} to remain, we must not choose 3 (because if we choose 3, we remove 2). But then, can we remove 2 by choosing another ball? The only other ball is 1, but 1 is (1,3). To remove 2 (2,1) by 1: we need a ball that is either both less or both greater. 1 is (1,3) and 2 is (2,1). 1 is not both less (1<2 and 3>1) and not both greater (1<2 and 3>1). So 1 cannot remove 2. Therefore, {2,3} can remain because we never choose 3 (so 2 is not removed) and we never choose 1 (so 2 is not removed by 1). But wait, the set {2,3} is not listed in the sample output. The sample output says the possible sets are {1,2,3}, {1,3}, and {1,2}. So {2,3} is not allowed.

    # Why? Because the operation can be performed any number of times, but the set {2,3} is not "closed" under the removal condition? Actually, the problem is asking for the sets that can be obtained by performing operations. The set {2,3} cannot be obtained because to obtain {2,3}, we must have removed 1. But to remove 1, we need a ball that dominates 1. The balls are 2 and 3. 2 is (2,1): 2>1 and 1<3? No, because 1 is (1,3). So 2 does not dominate 1 (we need both greater or both less). 3 is (3,2): 3>1 and 2<3, so not both greater. So no ball can remove 1. Therefore, the set {2,3} is not obtainable because we cannot remove 1 without a ball that dominates 1, and there isn't one. So the set {2,3} is not a valid set of remaining balls