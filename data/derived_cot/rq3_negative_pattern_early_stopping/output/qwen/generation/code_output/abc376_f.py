import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    q = int(data[1])
    instructions = []
    index = 2
    for i in range(q):
        h = data[index]; t = int(data[index+1]); index += 2
        instructions.append((h, t))
    
    # We'll use BFS for each instruction? But state space is n*n, which is 9e6, and q up to 3000, so that's 3000 * 9e6 which is 27e9 states, too slow.

    # Alternatively, we can use dynamic programming with state (l, r) and then update for each instruction.

    # But we need to compute the minimal operations to go from the previous state to the current state, with the constraint that at the end of each instruction, the specified hand is at the specified part.

    # We can precompute the minimal steps to move one hand from a to b on a ring of size n, which is min(|a-b|, n - |a-b|). But because the other hand might block, we have to consider that the other hand might be in the way.

    # However, note that the problem says: "it can be proved that any instructions are achievable". So we can assume that the minimal steps for one hand to move from a to b is the ring distance, but we might have to detour if the other hand is in the way.

    # But actually, the blocking condition only prevents moving to the other hand's current position. So if we want to move a hand from x to y, and the other hand is at z, then we can move the hand as long as we don't step on z. But if the path from x to y passes through z, then we have to go the other way.

    # So the minimal steps for one hand to move from x to y, given that the other hand is at z, is the minimal distance on the ring that doesn't go through z. But note that the other hand can move too, so we can coordinate.

    # Actually, the problem is more complex because both hands move and we can interleave moves. But the key is that the total operations is the sum of the moves of both hands.

    # Let me consider the state (l, r). We need to go from (1,2) to a sequence of states, each satisfying an instruction.

    # We can use Dijkstra or BFS in the state space (l, r) but 3000*3000=9e6 states, and each state has up to 4 edges (each hand can move two ways). So 9e6*4=36e6 edges, which is acceptable in C++ but in Python might be borderline. But we have 3000 instructions, so we can't run BFS for each instruction.

    # Alternatively, we can use a DP that stores the minimal operations to reach a state (l, r) after processing the first i instructions.

    # But the state space is 9e6, and 3000 instructions, so 3000*9e6=27e9 states, which is too many.

    # We need a smarter way.

    # Observation: The ring is symmetric and the constraints are local. Also, the two hands are independent except for the blocking condition.

    # Another idea: Instead of tracking both positions, we can track the positions relative to each other. But the absolute positions matter because of the instructions.

    # Alternatively, we can use a two-dimensional DP where dp[i][j] is the minimal operations to have left hand at i and right hand at j after processing the last instruction. Then we update from the previous instruction's states.

    # But the state space is 9e6, and 3000 instructions, so 3000*9e6 is 27e9, which is too slow in Python.

    # We need to optimize.

    # Let me think: The instructions are given in order. We start from (1,2). Then for each instruction, we must end at a state where the specified hand is at the specified part.

    # The minimal operations to go from a state (l, r) to a state (l', r') is the sum of the minimal steps for each hand to move from their current position to their target, but with the constraint that they don't pass through each other's starting position? Not exactly.

    # Actually, the minimal steps for one hand to move from a to b is the ring distance, but if the other hand is in the way, we might have to go the long way. But note: we can move both hands arbitrarily (