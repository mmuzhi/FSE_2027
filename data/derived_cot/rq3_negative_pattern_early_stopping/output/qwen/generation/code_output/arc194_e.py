def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    parts = data[0].split()
    n = int(parts[0])
    x = int(parts[1])
    y = int(parts[2])
    s = data[1].strip()
    t = data[2].strip()
    
    # If S is already T, return Yes.
    if s == t:
        print("Yes")
        return
        
    # Check if the total length condition holds for operations.
    # The operations require a segment of length x+y, so if n < x+y, then no operation can be performed, so we must have S == T.
    if n < x + y:
        print("No")
        return
        
    # We need to check if we can transform S to T by a series of operations.
    # Note: The operations are reversible and only change contiguous segments of length x+y.
    # Another observation: The operations can only change the string in specific patterns.
    # Let's consider the following: the operations can only change a segment of length x+y, and the changes are:
    # Operation A: changes [0^x, 1^y] to [1^y, 0^x]
    # Operation B: changes [1^y, 0^x] to [0^x, 1^y]
    #
    # But note: the operations can be applied multiple times and in any order, and they can overlap arbitrarily.
    #
    # However, note that the operations are local and the entire string might be broken into segments of length x+y, but the operations can overlap arbitrarily.
    #
    # Another idea: consider the string as a sequence of blocks of length (x+y). But the operations can change a block and the adjacent blocks might be affected if the operation overlaps.
    #
    # Alternatively, we can consider the following: the operations are essentially swapping two adjacent blocks of size y and x (with the condition that the first block is zeros and the second is ones for A, and vice versa for B). But note, the operation doesn't just swap the two blocks, it also inverts the bits? Actually, no: Operation A changes the first y characters (which were zeros) to ones, and the next x characters (which were ones) to zeros. So it's not a simple swap, but a transformation that depends on the current state.
    #
    # But note: the condition must hold for the operation to be applied. So we can only apply an operation if the segment is exactly [0^x, 1^y] for A and [1^y, 0^x] for B.
    #
    # Now, what are the necessary conditions for S to be transformed into T?
    #
    # Condition 1: The total number of ones in S and T must be the same? Actually, no: Operation A and B change the number of ones. Let's check:
    # Operation A: 
    #   Before: x zeros and y ones -> total ones = y.
    #   After: y ones and x zeros -> total ones = y (same) but wait, no: the operation changes the first y characters (from zeros to ones) and the next x characters (from ones to zeros). So the change in ones:
    #   - We add y ones (from zeros) and remove x ones (from ones to zeros). So net change: y - x.
    # Operation B:
    #   Before: y ones and x zeros -> total ones = y.
    #   After: x zeros and y ones -> total ones = y (same) but wait, the operation changes the first x characters (from ones to zeros) and the next y characters (from zeros to ones). So net change: -x + y.
    # So both operations change the total number of ones by (y - x). Therefore, the difference in the number of ones between S and T must be divisible by (y - x) and the quotient must be a non-negative integer (since we can only add (y-x) ones per operation, but note: we can do both operations, which change by (y-x) and (y-x) respectively? Actually, Operation A changes by (y - x) and Operation B changes by (y - x) as well? Wait, Operation A: net change = (y - x) because we add y ones and remove x ones. Operation B: net change = (y - x) because we add y ones (from zeros) and remove x ones (from ones to zeros). So both operations change the total number of ones by (y - x). Therefore, the difference (count_T - count_S) must be divisible by (y - x) and the quotient must be non-negative? Actually, no: we can do both operations,