import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    intervals = []
    index = 1
    for _ in range(n):
        L = int(data[index]); R = int(data[index+1]); index += 2
        intervals.append((L, R))
    
    q = int(data[index]); index += 1
    queries = []
    for _ in range(q):
        queries.append(int(data[index])); index += 1

    # We'll use a difference array to mark the effect of each contest.
    # However, note: the condition for a contest is checked at the current rating, which is the starting rating plus the number of previous triggers.

    # Instead, we can use a sweep-line over the entire range of ratings (from 1 to 500000) and simulate the contests in order.

    # But note: the contests are fixed and we are going to apply them in order. We can precompute an array "ans" for each starting rating from 1 to 500000.

    # However, the rating can increase beyond 500000, but the queries are only for starting ratings between 1 and 500000.

    # We can use a technique: 
    #   Let F(r) = the total number of contests that are triggered when starting at r.
    #   Then the final rating is r + F(r).

    # How to compute F(r) for all r from 1 to 500000?

    # We can use a "state" for each rating: the rating after each contest. But that is too heavy.

    # Alternate approach: 
    #   We can use a "jump" array that for each rating r, we know the next rating after processing all contests? But the contests are fixed.

    # Another idea: 
    #   We can use a "sweep" over the contests and update a Fenwick tree or segment tree for the entire range of ratings.

    # However, note the constraints: 
    #   N up to 200000, Q up to 300000, and rating from 1 to 500000.

    # We can precompute an array "dp" for the entire range of ratings (from 1 to 500000) that represents the total number of triggers that will occur from that rating onward.

    # But note: the contests are applied in order, so we can process the contests and update the rating.

    # Let's define an array "add" for each rating r (from 1 to 500000) that counts the total number of contests that will be triggered if we start at r.

    # We can use a difference array for the entire range of ratings (from 1 to 500000) and then use a two-pointer or binary search.

    # Actually, we can use a method similar to "sweep-line" for the contests:

    #   Let's define an array "events" for the entire range of ratings (from 1 to 500000) that marks the contests that start and end.

    # But note: the condition for a contest i is that the rating at the time of contest i is in [L_i, R_i]. The rating at contest i is the starting rating plus the number of previous contests that were triggered.

    # This is a sequential dependency.

    # We can use a different idea: 

    #   Let F(r) = the final rating after starting at r.
    #   Then F(r) = r + (number of contests i for which the condition holds at the time of contest i)

    #   The condition for contest i holds if and only if:
    #        r + (number of contests j (j < i) that were triggered) is in [L_i, R_i]

    #   Let T_i(r) = 1 if condition holds, else 0.

    #   Then F(r) = r + sum_{i=0}^{N-1} T_i(r)

    #   Now, note that the condition for contest i depends on the previous T_j(r) for j < i.

    #   We can try to compute the minimal rating that triggers a contest? 

    #   Let's define an array "next" for each contest i: 
    #        The condition for contest i is: r + (previous triggers) >= L_i and <= R_i.

    #   But the previous triggers depend on r.

    #   We can precompute for each contest i the minimal starting rating that would trigger contest i at least once? 

    #   Actually, we can use a "greedy