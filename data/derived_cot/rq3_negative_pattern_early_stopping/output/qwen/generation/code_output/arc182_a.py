import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    q = int(data[1])
    operations = []
    index = 2
    for i in range(q):
        p = int(data[index]); v = int(data[index+1]); index += 2
        operations.append((p, v))
    
    # We'll use dynamic programming. The idea is to consider the operations and the state of the array as the operations are performed.
    # However, the array is large (N up to 5000) and Q up to 5000, so we cannot keep track of the entire array.

    # Observation: The operations are assignments that set contiguous segments to a value. The condition for an operation is that the segment must not contain any value strictly greater than V_i.

    # Another observation: The operations are sequential and the array is updated. The key is that the array can be seen as having been updated by the operations, and the condition for an operation is that the current values in the segment are <= V_i.

    # We can think of the operations as defining a sequence of assignments. The array at the end is determined by the last operation that covers each index. But the condition must hold at the time of each operation.

    # Alternatively, we can think of the operations as events that set a segment to a value, and the condition is that at the time of an operation, the segment must not have any value greater than V_i. Since the array is initially zeros, and operations set entire segments, the condition for an operation is that the segment does not contain any value from a later operation that is greater than V_i? Actually, no: the condition is checked at the time of the operation, so the current values (from previous operations) must be <= V_i.

    # We can use a DP that goes operation by operation and keeps track of the "minimum" value that must be present in the array for the condition to hold? But that might not be sufficient.

    # Another idea: Instead of tracking the entire array, we can track the "effective" operations that have set values in the array. The condition for an operation is that the segment it is about to set does not contain any value from a previous operation that is greater than V_i. But note: if an operation sets a segment to a value, then that value might be overwritten by a later operation. However, the condition is checked at the time of the operation, so we only care about the current state.

    # We can use a segment tree or a Fenwick tree to keep track of the maximum value in a segment? But then we have to update and query, and Q and N are up to 5000, so that might be acceptable. But then we have 2^Q possibilities, which is too many.

    # Alternatively, we can use a state machine that tracks the "last" operation that affects each part of the array. But that is also too complex.

    # Let me think of the necessary conditions for an operation to be allowed.

    # Operation i (with parameters p_i, v_i) can be of two types. Let's denote:
    #   Type1: [1, p_i] must not have any element > v_i.
    #   Type2: [p_i, n] must not have any element > v_i.

    # The array is built from previous operations. The array is initially zeros.

    # We can consider that the array is divided into segments by the operations. But the operations are not necessarily covering the entire array.

    # Another idea: Instead of thinking about the entire array, we can think about the operations and the constraints they impose on the previous operations.

    # Condition for operation i (if we choose type1): The segment [1, p_i] must have all values <= v_i. Similarly for type2.

    # The values in the array are set by previous operations. Each previous operation j (with parameters p_j, v_j) that overlaps with [1, p_i] must have set that part to v_j, and note that if an operation j sets a segment that overlaps [1, p_i] and has v_j > v_i, then at the time of operation i, the segment [1, p_i] would have a value v_j (from operation j) which is > v_i, so operation i would be invalid.

    # But wait, operation j might have been overwritten by a later operation? Actually, no: the operations are sequential. Operation j happens before operation i, so the value set by operation j is still there unless operation i or a later operation overwrites it. But we are only concerned with the state at the time of operation i.

    # However, the