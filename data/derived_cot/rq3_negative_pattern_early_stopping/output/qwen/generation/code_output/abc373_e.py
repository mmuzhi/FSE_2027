import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    A = list(map(int, data[3:3+n]))
    
    total_counted = sum(A)
    remaining_votes = k - total_counted
    
    # If a candidate already satisfies the condition, then we can set C_i = 0.
    # But note: the condition is about the number of candidates with more votes. 
    # We need to consider the worst-case distribution of the remaining votes.
    
    # Step 1: Sort the candidates by their current votes.
    A_sorted = sorted(A)
    
    # We'll create an array for the answers for each candidate.
    # But note: the condition depends on the entire set of votes.
    # We need to consider the other candidates and how the remaining votes can be distributed to harm candidate i.
    
    # Let's define a function to compute the minimum X for a candidate i.
    # However, doing this individually for each candidate might be too slow (N up to 200,000). We need a more efficient method.
    
    # Idea: 
    # For candidate i, let v = A_i + X.
    # We need to ensure that the number of candidates j (j != i) with A_j + (additional votes) > v is less than M.
    # But the additional votes for other candidates can be arbitrarily distributed (total remaining is T - X).
    # The worst-case for candidate i is when we try to maximize the number of candidates j with A_j + (votes) > v.
    # But note: we can only assign T - X votes to the other candidates.
    
    # However, we can also consider that some candidates might already have more than v (even without additional votes). Let's call these candidates "already above".
    # Then, we need to consider the remaining candidates (not already above) and assign votes to as many as possible to exceed v, but without exceeding the total remaining votes.
    
    # Alternatively, we can think: what is the maximum number of candidates that can be made to have more than v (including those already above) with the remaining T - X votes?
    # But note: the condition is independent of the votes assigned to candidate i (since we are giving X to candidate i). The remaining votes are T - X.
    
    # Actually, the condition for candidate i is: the number of candidates j (j != i) with final votes > v must be < M.
    # The final votes for candidate j are A_j + (votes assigned to j). The total votes assigned to other candidates is T - X.
    
    # The worst-case scenario is to assign as few votes as possible to as many candidates as possible to just exceed v, but we can also assign more to fewer candidates? Actually, to maximize the count of candidates with more than v, we should assign the minimal required votes to each candidate to just exceed v, and then distribute the rest arbitrarily (but that doesn't help in increasing the count). So, the minimal votes needed to make a candidate j (with A_j <= v) exceed v is max(0, v - A_j + 1). But if A_j > v, then no votes are needed (they are already above).
    
    # So, the problem reduces to: 
    # Let v = A_i + X.
    # Let S be the set of candidates j (j != i) with A_j > v. (already above)
    # Then, for the remaining candidates (not in S and not i), we need to assign at least (v - A_j + 1) votes to each to make them above. But we can only assign T - X votes in total to these candidates (and also to those already above? Actually, we can assign any number to any candidate, but the goal is to maximize the count of candidates above v. So, we would assign the minimal required to as many candidates as possible to get them above.
    
    # However, note: we can also assign votes to the already above candidates, but that doesn't help in increasing the count (they are already above). So, we focus on the candidates that are not already above and not candidate i.
    
    # Let R = T - X (remaining votes for others).
    # Let B = [A_j for j != i and A_j <= v]  (the candidates that can be pushed above by assigning some votes)
    # For each candidate j in B, the minimal votes needed to push them above is (v - A_j + 1). But note: we can also assign more than that, but to maximize the count, we assign exactly that minimal amount to as many as possible until we run out of votes.
    
    # The maximum number of candidates