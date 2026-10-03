import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().split()
    if not data:
        print("0" * int(data[0]) if data else "0"*0)
        return
    
    it = iter(data)
    n = int(next(it)); m = int(next(it))
    
    # Build graph for 2-SAT? Or use linear algebra?
    # But note: the equations are linear in GF(2) with variables h_i (0/1) and s_i (0/1) is chosen.
    # However, the equations for C_i=0 are fixed, and for C_i=1 depend on s_{A_i}.
    # We can try to model as a 2-SAT problem by introducing variables for h_i and s_i, but note s_i is chosen and h_i is assigned.
    # Alternatively, we can consider that the condition for each testimony is a constraint between h_{A_i} and h_{B_i} that depends on s_{A_i}.
    # But note: s_{A_i} is chosen, so for each testimony, the constraint is either one of two types.
    #
    # Let me define two types of constraints for a testimony (A_i, B_i, C_i):
    #   If C_i = 0: then the constraint is h_{A_i} = 1 - h_{B_i}
    #   If C_i = 1: then the constraint is either h_{A_i} = h_{B_i} or h_{A_i} = 1 - h_{B_i} (depending on s_{A_i})
    #
    # But note: the choice of s_{A_i} is global. So we have to choose one set S for all.
    #
    # We can think of it as: we have to assign to each villager i a bit s_i (0 or 1). Then, for each testimony, we have an equation that must be satisfied by the h_i's.
    #
    # The equations are:
    #   For C_i=0: h_{A_i} + h_{B_i} = 1 (mod 2)
    #   For C_i=1: h_{A_i} + h_{B_i} = s_{A_i} (mod 2)
    #
    # But wait, the equation for C_i=1 is: h_{A_i} = h_{B_i} XOR s_{A_i}, which is equivalent to h_{A_i} + h_{B_i} + s_{A_i} = 0 (mod 2) is not correct.
    #
    # Actually, the equation h_{A_i} = h_{B_i} XOR s_{A_i} is equivalent to:
    #   h_{A_i} + h_{B_i} + s_{A_i} = 0 (mod 2) is not correct.
    #
    # Let me re-derive:
    #   h_{A_i} = h_{B_i} XOR s_{A_i}
    #   => h_{A_i} = h_{B_i} + s_{A_i} (mod 2)   [because XOR is addition in GF(2)]
    #   => h_{A_i} + h_{B_i} + s_{A_i} = 0 (mod 2)
    #
    # But wait, that is correct. Because if you have a = b + c (mod 2), then a + b + c = 0 (mod 2) is not true. Actually, a + b + c = (a + b + c) mod 2. And if a = b + c, then a + b + c = (b + c) + b + c = 2b + 2c = 0 (mod 2). 
    #
    # So the equation h_{A_i} = h_{B_i} + s_{A_i} (mod 2) is equivalent to h_{A_i} + h_{B_i} + s_{A_i} = 0 (mod 2) is not correct. 
    #
    # Actually, the equation h_{A_i} = h_{B_i} + s_{A_i} (mod 2) is equivalent to:
    #   h_{A_i} + h_{B_i} + s_{A_i} = 0 (mod 2) is not the same as the equation.
    #
    # Let me test with numbers:
    #   Case 1: h_{A_i}=0, h_{B_i}=0, s_{A_i}=0: 0 = 0+0 -> 0=0, and 0+0+0=0 -> holds.
    #   Case 2: h_{A_i}=