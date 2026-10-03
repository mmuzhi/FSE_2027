import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        print(0)
        return
    n, q = map(int, data[0].split())
    instructions = []
    for i in range(1, q+1):
        parts = data[i].split()
        if len(parts) < 2:
            continue
        h = parts[0]
        t = int(parts[1])
        instructions.append((h, t))
    
    # Initial state: left hand at 1, right hand at 2.
    l, r = 1, 2
    total_ops = 0

    for i in range(q):
        h, t = instructions[i]
        # If the target is already at the specified hand, then 0 operations.
        if h == 'L':
            if l == t:
                # Then we don't need to move the left hand, but note: the right hand must remain fixed (which it is).
                # However, we must check: is the right hand at the target? No, because the instruction condition says T_i != r_i (for H_i='L', T_i != r_i). So we are safe.
                # But note: the state is (l, r) and we are only moving the left hand. The right hand is fixed. So if l==t, then we are done.
                # But what if the right hand is at t? Then the instruction condition says T_i != r_i, so that case is excluded.
                # So we can just leave it.
                continue
            else:
                # We need to move the left hand from l to t, avoiding the right hand (which is fixed at r).
                # We have two directions: clockwise and counterclockwise.
                # We'll compute the minimal steps to go from l to t without stepping on r.

                # First, compute the two distances without obstacle.
                # Let d1 = clockwise distance from l to t (without considering r)
                d_clockwise = (t - l) % n
                if d_clockwise < 0:
                    d_clockwise += n
                d_counterclockwise = n - d_clockwise

                # Now, check if the clockwise path from l to t passes through r.
                # The clockwise path: we go from l to l+1, l+2, ... until t (mod n).
                # We need to check if r is in the set of nodes from l to t (in the clockwise direction) excluding the start (l) and including the end (t) is not allowed because we are moving to t (and t is not r by condition) but the condition is that we cannot step on r during the moves.

                # Actually, we are allowed to step on t (the target) because the instruction condition says T_i != r_i (so t != r) and the operation condition only forbids stepping on the other hand (which is r) during the move. So we can step on t.

                # But note: the operation condition: "the other hand is not on the destination part" — so when we move to a destination, we must not have the other hand there. But the destination is t, and we know t != r (by the problem condition). So the only forbidden node is r.

                # So we must avoid r.

                # How to check if the clockwise path from l to t (without wrap) passes through r?
                # We can consider the circle as a linear array from 1 to n, and then wrap.

                # Alternatively, we can consider two cases: 
                #   Case 1: l <= t
                #       Then the clockwise path goes from l to t, and the nodes are [l, l+1, ..., t] (if l<=t). But note: if l<=t, then the clockwise path is the direct one.
                #   Case 2: l > t
                #       Then the clockwise path goes from l to n, then wraps to 1 and goes to t.

                # But note: we are using modulo arithmetic. We can define a function to check if a node x is between l and t in the clockwise direction.

                # Let's define a function: is_between_clockwise(a, b, x, n):
                #   If a <= b:
                #       then x is between a and b (inclusive) if a <= x <= b.
                #   Else (a > b):
                #       then x is between a and b (inclusive) if x >= a or x <= b.

                # But note: we are moving from a to b (clockwise) and we are allowed to step on a (the start) but not on r (which is forbidden). The forbidden node r must not be in the set of nodes we step on (except the