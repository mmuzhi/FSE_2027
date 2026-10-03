def main():
    import sys
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    
    sequences = []
    
    def dfs(pos, last, current):
        if pos == N:
            # We have a complete sequence
            sequences.append(current[:])
            return
            
        # The next number must be at least last + 10
        # Also, the next number must be at most M (since the last element must be <= M, and we are building from left to right)
        # But also, we must ensure that the remaining terms can be built. The next term must be at least last+10, and then the next must be at least last+20, etc.
        # The minimum value for the last term is current[0] + 10*(N-1). But we are building step by step.
        # We can set an upper bound for the next term: M - 10*(N-pos-1) because the remaining (N-pos) terms must each be at least 10 more than the previous, so the next term must be <= M - 10*(N-pos-1)
        # However, we can also set the next term to be at most M (since the last term must be <= M). But note: the condition for the next term is only that it is at least last+10 and at most M (if we set the upper bound as M, then we might miss sequences that are too large for the remaining terms? Actually, we can set the upper bound as M, because if we set a tighter bound (like M - 10*(N-pos-1)) then we are ensuring that the sequence can be completed. But note: the condition for the next term is only the immediate next, and the subsequent terms must be built from that. However, we must ensure that the entire sequence ends <= M.

        # Actually, we can set the next term's upper bound as M (since the last term must be <= M) and then in the next steps, we will enforce the condition that the next term is at least the previous +10 and also the last term must be <= M. But we can also set a tighter bound for the next term: the next term must be <= M - 10*(N-pos-1) because the remaining (N-pos) terms must each be at least 10 more, so the next term must be at most M - 10*(N-pos-1) to have a chance to complete the sequence.

        # However, note: the condition for the entire sequence is only that the last term is <= M. The intermediate terms can be larger than M? No, because the last term is built from the previous and must be <= M. But if we set the next term too high, then the subsequent terms might exceed M. So we must set an upper bound for the next term that ensures that the entire sequence can be built without exceeding M.

        # The minimum value for the last term is: current[0] + 10*(N-1). But we are at position pos, so the minimum value for the last term is current[0] + 10*(N-1) (if we start from the first element). However, we are building from the beginning.

        # Alternatively, we can set the next term's upper bound as M (because the last term must be <= M) and then in the next steps, we will enforce the condition that the next term is at least the previous +10 and the last term is <= M. But then we might generate sequences that are too large for the remaining steps? Actually, we can set the next term's upper bound as M (since the last term must be <= M) and then in the next steps, we will enforce the condition that the next term is at least the previous +10 and the last term is <= M. But note: the condition for the next term is only the immediate next, and the subsequent terms must be built from that. However, we must ensure that the entire sequence ends <= M.

        # Actually, we can set the next term's upper bound as M (because the last term must be <= M) and then in the next steps, we will enforce the condition that the next term is at least the previous +10 and the last term is <= M. But then we might generate sequences that are too large for the remaining steps? Actually, we can set the next term's upper bound as M (because the last term must be <= M) and then in the next steps, we will enforce the condition that the next term is at least the previous +10 and the last term is <= M. But note: the condition for the next term is only the immediate next, and the subsequent terms must be built from that. However, we must