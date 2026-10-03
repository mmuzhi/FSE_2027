import sys
from collections import defaultdict
from math import gcd
import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    p = list(map(int, data[2:2+n]))
    
    # If k == 0, then we output the original p.
    # But note: k can be 0, but the problem says K>=1, but constraints say K>=1, but sample input 2 has K=1000000000000000000, so we must handle large K.

    # We can convert the permutation to a 0-indexed permutation Q.
    # But note: the operation is defined on the array P (1-indexed). We can work with the 0-indexed representation.

    # However, we can also note: the operation is equivalent to composing the permutation (in terms of the 0-indexed indices) twice.

    # Steps:
    # 1. Build the graph (cycle decomposition) of the permutation (0-indexed).
    # 2. For each cycle of length L, the operation (which is a composition of the permutation with itself) is equivalent to moving two steps in the cycle? Actually, no: the operation is composing the permutation with itself, so the cycle length for the new permutation is the order of the permutation raised to the power 2.

    # Actually, the operation is: 
    #   Let f be the permutation (0-indexed). Then the operation is f^2 (composing f with itself).

    # Then after K operations, we have f^(2^K) ? 

    # But wait: 
    #   Operation 1: f^2
    #   Operation 2: (f^2)^2 = f^4
    #   Operation 3: f^8
    #   So after K operations, we have f^(2^K) ?

    # However, note: the operation is defined as: 
    #   Operation 1: T = f^2
    #   Operation 2: T^2 = (f^2)^2 = f^4
    #   Operation 3: T^3 = (f^2)^3 = f^8? 

    # But wait, the operation is defined as: 
    #   Operation 1: T = f^2
    #   Operation 2: T = T composed with T = f^4
    #   Operation 3: T = T composed with T = f^8

    # So the exponent is 2^K.

    # However, note: the operation is defined as: 
    #   Operation 1: T = f^2
    #   Operation 2: T = f^4
    #   Operation 3: T = f^8

    # But wait, the operation is defined as: 
    #   Operation 1: T = f^2
    #   Operation 2: T = T composed with T = (f^2) composed with (f^2) = f^4
    #   Operation 3: T = T composed with T = (f^4) composed with (f^4) = f^8

    # So the exponent is 2^K.

    # However, note: the operation is defined on the permutation as a function. The permutation f has a cycle decomposition. The order of the permutation is the least common multiple (LCM) of the cycle lengths. Then the exponentiation f^(2^K) is periodic with period LCM(cycle_lengths). 

    # But note: 2^K can be huge (K up to 10^18). We cannot compute 2^K directly.

    # However, note: the operation is defined as: 
    #   Operation 1: f^2
    #   Operation 2: f^4
    #   Operation 3: f^8

    # So the exponent is 2^K. But note: the permutation f has a cycle decomposition. The effect of f^(2^K) on a cycle of length L is to advance each element by (2^K mod L) steps.

    # But note: the operation is defined as: 
    #   Operation 1: f^2
    #   Operation 2: f^4
    #   Operation 3: f^8

    # So the exponent is 2^K. However, we can reduce the exponent modulo the order of the permutation? 

    # Actually, the order of the permutation is the LCM of the cycle lengths. But note: the operation is not the identity until the exponent is a multiple of the order. However, we are not raising to the power of the order, but to the power of 2