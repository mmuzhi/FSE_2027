import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    parts = data[0].split()
    n = int(parts[0])
    R = int(parts[1])
    C = int(parts[2])
    S = data[1].strip()
    
    # We are going to compute for each t from 1 to n (i.e., time t+0.5) whether there is smoke at (R, C)
    # We note that the smoke at (R, C) at time t+0.5 can come from:
    #   - The initial particle that started at (0,0) and moved t steps (if the net displacement equals (R, C))
    #   - Or from a particle added at step k (1<=k<=t) and then moved (t - k) steps (if the net displacement of the substring S[k-1:t] equals (R, C) and the condition for adding the particle holds)
    #
    # However, note that the condition for adding a particle at step k is that (0,0) was empty after the wind at step k. But note: the state at step k (after the wind) is determined by the previous steps. This seems complex.
    #
    # Alternate Insight:
    # The smoke at (R, C) at time t+0.5 is present if and only if:
    #   There exists an integer k (0<=k<=t) such that:
    #       Let m = t - k   (number of steps the particle moved)
    #       The displacement caused by the substring S[k:m] (if k is the step index, then the substring from index k to t-1) equals (R, C) and the particle was added at step k.
    #
    # But note: the particle added at step k (if k>=1) is added only if (0,0) was empty after the wind at step k. However, the state at step k (after the wind) is determined by the previous steps. But note: the particle added at step k is independent of the previous steps? Actually, no: the condition for adding is that (0,0) is empty. But the condition for (0,0) being empty at step k is that the net displacement of the initial particle (and any previous added particles) after k steps is not (0,0). 
    #
    # This seems too complex to simulate for each t and k.
    #
    # Another Insight: Reverse the problem. Instead of tracking the smoke, track the origin of the smoke at (R, C) at time t+0.5.
    # A smoke particle at (R, C) at time t+0.5 must have come from a cell (r0, c0) at time (t-1)+0.5 (i.e., the previous state) by moving in the direction opposite to the wind at step t. But wait, the wind at step t moves the smoke from the state at time t-0.5 to time t+0.5. So, to be at (R, C) at time t+0.5, the particle must have been at (R', C') at time t-0.5 such that:
    #   If S[t-1] is 'N', then (R', C') = (R+1, C) because moving N from (R+1, C) would go to (R, C).
    #   Similarly, for 'S': (R-1, C), 'W': (R, C+1), 'E': (R, C-1).
    #
    # But note: the state at time t-0.5 is the state after the wind at step t-1 (if t>=2) and then the condition for adding a particle at step t-1 (if (0,0) was empty) is already accounted for. However, the particle at (R, C) at time t+0.5 could also be the one added at step t (if t<=n) and then hasn't moved (if t is the current step, then the particle added at step t is at (0,0) and then we check: but wait, the particle added at step t is at (0,0) at time t+0.5, so unless (R, C) is (0,0), it doesn't contribute. But note: the problem states (R, C) != (0,0). So, we don't have to worry about (0,0) for the current step's added particle.
    #
    # Actually, the particle added at step t is at (0,0) at time t+0.5. So, if (R, C) is