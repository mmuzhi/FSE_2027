import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # We are to find the maximum length of a contiguous subarray that is a 1122 sequence.
    # We can use a two-pointer approach or dynamic programming. However, note that the condition requires:
    #   - The subarray has even length.
    #   - It is broken into consecutive pairs (each pair two same numbers).
    #   - Each number in the subarray appears exactly twice (so if a number appears, it must appear in two pairs).

    # But note: the condition does not require that the two occurrences of a number are consecutive. However, the pairs are consecutive.

    # Let's think: 
    #   We can traverse and try to extend a subarray and check the conditions. But the constraints are up to 200,000.

    # Alternate approach:
    #   We note that the sequence must be of the form: [x1, x1, x2, x2, x3, x3, ...] and the entire subarray must have each distinct number exactly twice.

    # However, note: the pairs must be consecutive. So the subarray must be broken into consecutive pairs.

    # We can use a two-pointer and a frequency map for the current window, but we must also check that the window is broken into pairs.

    # But note: the condition for a valid 1122 sequence is:
    #   Let the window be of length L (even). Then for each i from 0 to L-1, we can group into pairs: (A[i], A[i+1]), (A[i+2], A[i+3]), ... 
    #   and each pair must have two equal numbers.

    # However, we can also note: the entire window must have each number appearing exactly twice. But wait, consider [1,1,2,2,3,3] -> valid. But what if we have [1,1,2,2,1,1]? 
    #   Then the window [1,1,2,2,1,1] has 1 appearing 4 times -> invalid.

    # So the condition is: 
    #   The window must be broken into pairs (so consecutive two) and each distinct number must appear exactly twice.

    # But note: the pairs are consecutive. So the window must be of even length and for every two consecutive elements (at positions 0,1; 2,3; ...) the two elements must be equal.

    # However, wait: the problem does not require that the pairs are of distinct numbers. It only requires that the entire sequence (the window) has each number exactly twice.

    # Example: [1,1,2,2] -> valid.
    # Example: [1,1,1,1] -> invalid because 1 appears 4 times.

    # Therefore, we can do:
    #   We want to find the longest contiguous even-length subarray such that:
    #       1. For every j from 0 to L/2-1, A[2j] == A[2j+1].
    #       2. In the entire subarray, each number appears exactly twice.

    # But note: condition 1 is necessary for the pairs. Condition 2 is global.

    # However, condition 1 implies that the entire subarray is broken into pairs of equal numbers. Then condition 2 requires that no number appears more than twice. But note: if a number appears in two different pairs, then it appears twice. And if a number appears only once, then it would break condition 1 because the two occurrences must be in two different pairs (so the number must appear twice). Actually, condition 2 says "either not at all or exactly twice", so if a number appears, it must appear twice. And condition 1 requires that the pairs are consecutive and each pair is two same numbers. 

    # But note: condition 1 does not require that the two same numbers in a pair are distinct from the two same numbers in another pair. So the same number can appear in two different pairs. 

    # However, condition 2 requires that the entire subarray has each number exactly twice. So if a number appears in two pairs, that's two occurrences. But if a number appears in three pairs, then it would be six occurrences? Actually, no: condition 1 breaks the subarray into pairs. Each pair is two same numbers. So if a number appears in three pairs, then it appears 6 times. But condition 2 requires exactly two. 

    # Therefore, the entire subarray must have exactly two pairs for each distinct