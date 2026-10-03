import sys

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); m = int(next(it)); q = int(next(it))
    people = []
    for _ in range(m):
        s = int(next(it)); t = int(next(it))
        people.append((s, t))
    
    queries = []
    for _ in range(q):
        l = int(next(it)); r = int(next(it))
        queries.append((l, r))
    
    # We need to preprocess the people to determine the constraints on the roads.
    # However, note that the problem is very complex and requires a different approach.
    # After reading sample solutions and known techniques, one common approach is to use a greedy method or segment tree to track the constraints.

    # But note: the problem is non‐trivial. We need to find a way to represent the constraints and then answer the queries.

    # Insight: Each person's journey imposes two conditions:
    #   1. The sum of the roads in the segment is 0.
    #   2. The minimal prefix sum (forward) is at least 1.

    # However, note that the condition for the reverse journey is not required because the journey is fixed.

    # But wait, the problem states that the person's journey is from S_i to T_i. The condition is that at every intermediate town the stamina is positive. This is equivalent to:
    #   Let the segment be from a to b (with a < b). Then the cumulative sums from a to b-1 must be positive and the total sum from a to b-1 is 0.

    # Now, note that the condition for the entire segment being 0 and the minimal prefix being positive is a very strong condition.

    # Another insight: We can think of the journey as a path that starts at 0, ends at 0, and never drops below 1 in between. This is similar to a Dyck path or a balanced parentheses, but with arbitrary integers.

    # However, note that the roads can be negative. But the condition requires that the cumulative sum never drops below 1 (until the last step, which is 0). 

    # Actually, the condition is that the cumulative sum at each intermediate step is at least 1, and the final cumulative sum is 0.

    # This is a very strong condition. In fact, the entire segment must have a total sum of 0 and the minimal value of the cumulative sums (excluding the last) must be at least 1.

    # Now, consider two people: 
    #   Person 1: from a to b (a < b)
    #   Person 2: from c to d (c < d)

    # The roads are shared. We need to assign integers to the roads such that both conditions hold.

    # But note: the condition for Person 1 is that the sum from a to b-1 is 0 and the minimal prefix from a is at least 1.
    # Similarly for Person 2.

    # However, the problem is asking for a single setting of the roads that satisfies all people in the query range.

    # This is a system of linear equations and inequalities. But the number of variables (n-1) and constraints (m) is too large.

    # We need a different approach.

    # Known similar problems: "Traffic" or "Roads" in competitive programming, often solved with greedy or segment tree.

    # Another idea: Instead of thinking about the roads, think about the towns. Each person's journey is a contiguous segment. The condition is that the segment has a total sum of 0 and the minimal prefix is at least 1.

    # But note: the roads are between towns. The stamina change is additive. 

    # Let's define an array d[1..n] (or 0-indexed) such that d[i] is the stamina at town i. Then for a person from S_i to T_i (S_i < T_i):
    #   d[S_i] = 0
    #   d[S_i+1] = d[S_i] + w_{S_i} = w_{S_i} >= 1
    #   d[S_i+2] = d[S_i+1] + w_{S_i+1} >= 1
    #   ...
    #   d[T_i] = 0

    # And the condition is that d[j] >= 1 for all j from S_i+1 to T_i-1.

    # Now, note that the road strengths are the differences: w_j = d[j+1] - d[j].

    # Then the condition for the entire segment is:
    #   d[T_i] - d[S_i] = 0, which is given.
    #   And d[j] >=