import math

def main():
    import sys
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        N = int(data[index]); index += 1
        K = int(data[index]); index += 1
        
        # The key observation: the entire coloring must be symmetric with respect to the line of the operator at each step.
        # The symmetry condition forces that if a point x is colored, then the symmetric point (with respect to the operator's line) must be colored (if it exists) at the same time or already.

        # However, note: the operators alternate, and the starting operator is Alice at 0. Then Bob at K, then Alice again, etc.

        # The symmetry condition for a given operator at position p is: the coloring must be symmetric about the line through p and the center.

        # The reflection of a point x about the line through p is: 
        #   Let d = (p - x) mod N, then the reflection is p + (p - x) mod N? 
        #   Actually, the reflection of x about p is: 
        #       y = (2*p - x) mod N   (but then we adjust to be in [0, N-1])

        # But note: the circle is symmetric, and the reflection must be a point on the circle. However, the operation is defined for any white point. 

        # The problem is cooperative and they want to maximize the number of black points.

        # Let's think about the entire process:

        # The symmetry condition must hold at every step. Therefore, the coloring is always symmetric about the line of the current operator.

        # The entire coloring must be symmetric about the line of the operator at the time of the operation.

        # However, note: the operations are done in alternating turns, and the operators are fixed (Alice at 0, Bob at K). But the symmetry condition is defined by the operator's current position.

        # Actually, the problem states: "the straight line connecting the operator and the center". So the operator's position is fixed for each turn: first Alice (at 0), then Bob (at K), then Alice (at 0), then Bob (at K), etc.

        # Therefore, the symmetry condition alternates between two symmetries: 
        #   First symmetry: about the line through 0.
        #   Second symmetry: about the line through K.

        # But note: the entire coloring must be symmetric with respect to the last operator's line? Actually, the condition is that after each operation, the coloring is symmetric with respect to the line of the operator who just moved.

        # However, the problem does not say that the symmetry condition must hold for all previous operators. It says "the coloring of the points must be symmetric with respect to the straight line connecting the operator and the center".

        # So after Bob's turn, the coloring must be symmetric about the line through K. Then after Alice's next turn, it must be symmetric about the line through 0.

        # This is a key point: the symmetry condition is reset to the operator's line at each turn.

        # Therefore, the coloring must be symmetric about the line of the operator who just moved.

        # Now, what does that imply?

        # Let the current operator be at p. Then, for every black point x, the reflection of x about p must be black (if it exists). But note: the reflection of x about p is defined as (2*p - x) mod N, but we have to adjust to be in [0, N-1]. 

        # However, note: the circle has rotational symmetry, but the reflection operation is defined by the line through p. 

        # The reflection operation is an involution, and the set of black points must be a union of orbits under the reflection. But note: the reflection about p is an operation that pairs points (unless a point is fixed, i.e., x = p, then the reflection is p itself). 

        # But wait: if we reflect a point x about p, we get y = (2*p - x) mod N. Then reflecting y about p gives x. So the black points must be closed under reflection about p.

        # However, the condition is only that the coloring is symmetric about p at the moment of the operation. But note: the operations are sequential and the symmetry condition is reset at each turn.

        # Actually, the problem says: "after the operation, the coloring of the points must be symmetric with respect to the straight line connecting the operator and the center".

        # So at the moment after an operation, the coloring is symmetric about the operator's line. Then the next operation must be symmetric about the next operator's line.

        # This means that the coloring must be