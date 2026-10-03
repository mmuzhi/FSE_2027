import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print("No")
        return
    
    it = iter(data)
    N = int(next(it)); M = int(next(it)); A = int(next(it)); B = int(next(it))
    intervals = []
    for _ in range(M):
        L = int(next(it)); R = int(next(it))
        intervals.append((L, R))
    
    # Build safe segments
    safe_segments = []
    # First safe segment: from 1 to intervals[0][0]-1, if exists
    if M == 0:
        # Only one safe segment: [1, N]
        safe_segments.append((1, N))
    else:
        # First safe segment: [1, intervals[0][0]-1]
        if intervals[0][0] > 1:
            safe_segments.append((1, intervals[0][0]-1))
        
        # Middle safe segments
        for i in range(M-1):
            start = intervals[i][1] + 1
            end = intervals[i+1][0] - 1
            if start <= end:
                safe_segments.append((start, end))
                
        # Last safe segment: [intervals[-1][1]+1, N]
        if intervals[-1][1] < N:
            safe_segments.append((intervals[-1][1]+1, N))
    
    # If the first safe segment does not contain 1, then we cannot start. But by construction, the first safe segment is [1, ...] if there is a bad interval starting at >1, otherwise the first safe segment is [1, N] (if M==0) or [1, intervals[0][0]-1] (if intervals[0][0]>1). So we are safe.
    
    # Now, we have safe_segments. We wish to know if we can go from the first safe segment to the last safe segment by steps of size between A and B.
    
    # We'll do a BFS on the safe_segments. Each node is a safe segment (represented by its index). We start from the segment that contains 1 (which is the first one, because 1 is the smallest and the first safe segment starts at 1) and we wish to reach the last safe segment (which contains N).
    
    # But note: the first safe segment might not be the one that contains 1? Actually, we built the safe_segments such that the first one starts at 1. So the first safe segment is the one containing 1.
    
    # We'll use a queue and a visited set for segment indices.
    from collections import deque
    n_segments = len(safe_segments)
    visited = [False] * n_segments
    # We'll also precompute the next safe segments that are reachable from the current one. But note: we can jump from a segment i to a segment j (j>i) if the jump from the current segment can reach segment j.
    # Condition: the current segment i has [s_i, e_i]. The reachable range is [s_i+A, e_i+B]. We require that this range overlaps with segment j (which is [s_j, e_j]).
    # But note: the safe segments are in increasing order and the bad intervals are in between. So the next safe segment j must be the next one (or later) and the condition is that the current segment's reachable range must cover at least the start of the next safe segment j.
    # However, we can jump to any safe segment j (with j>i) that is contained in [s_i+A, e_i+B]. But note: the safe segments are contiguous and separated by bad intervals, so we can only land in one safe segment at a time.
    
    # But note: the reachable range [s_i+A, e_i+B] might cover multiple safe segments. We can jump to any safe segment that is contained in that range. However, we must not jump over a safe segment and land in a bad one? Actually, we can only land in a safe segment. And the safe segments are the only safe squares.
    
    # We can do: for each segment i, we can compute the maximum reachable position: e_i+B. Then, we can find the next safe segment that starts at <= e_i+B. But note: we can also jump to a safe segment that starts at a position greater than e_i+B? No, because we cannot jump beyond e_i+B. So we can only reach safe segments that start at <= e_i+B.
    
    # However, we must also ensure that the jump does not land in a bad square. But by the definition of safe_segments, if we land in a safe segment, then it's safe. And the jump from the current segment must land in a safe segment. But note: