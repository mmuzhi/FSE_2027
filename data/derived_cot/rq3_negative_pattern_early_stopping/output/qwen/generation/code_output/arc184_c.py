def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    # We are to find the maximum f(i) for i in [1, 2**100 - A[-1] - 1]
    # But note: 2**100 is too big to iterate.
    # We need to find a pattern or mathematical insight.

    # Observation: The crease types are periodic or determined by the binary representation.

    # However, note that the problem is about folding 100 times. The creases are at positions 1 to 2**100 - 1.
    # The type of a crease at position x (1-indexed) can be determined by the binary representation of x-1 (0-indexed) with 100 bits.

    # Actually, in the folding process, the type of the crease is determined by the number of times the folding path goes left or right.

    # There is a known result: the k-th crease (0-indexed) is a mountain fold if the number of 1s in the binary representation of k is even, and valley if odd? Or vice versa?

    # Let me check with a small example (n=2 folds, so 3 creases, positions 0,1,2 (0-indexed) or 1,2,3 (1-indexed)).

    # For n=2 folds, the creases are at positions 1,2,3 (1-indexed). The types are given in the sample as a contiguous subsequence "MMVM" (from the problem statement). But wait, the sample input has A = [0,1,2,3] and the answer is 3.

    # Actually, the problem says: "There is a contiguous subsequence of creases like MMVM. There is no contiguous subsequence like MMMM, so the answer is 3."

    # So, for the entire paper (with 2^100 - 1 creases), we are to find the maximum number of mountain folds in any contiguous subsequence of length N (which is 4 in the sample) that starts at some i.

    # But wait, the problem says: "For each integer i from 1 through 2^{100} - A_N - 1, define f(i) as follows: the number of k = 1, 2, \dots, N such that the (i + A_k)-th crease from the left is a mountain fold."

    # So, for each i, we look at the creases at positions i + A_1, i + A_2, ..., i + A_N. In the sample, A = [0,1,2,3], so we look at i, i+1, i+2, i+3.

    # And we want the maximum f(i) over i.

    # The sample output is 3.

    # So, the maximum number of mountain folds in any 4 consecutive creases is 3.

    # Now, how to compute this without iterating over 2^100 positions?

    # We need to know the type of each crease (mountain or valley) as a function of its position (from 1 to 2^100 - 1).

    # The type of the crease at position x (1-indexed) can be determined by the binary representation of x-1 (0-indexed) with exactly 100 bits (padding with zeros on the left).

    # Specifically, the type is determined by the parity (even or odd) of the number of 1s in the binary representation of x-1.

    # But wait, is that correct? Let me test with n=2 (2 folds, so 3 creases). The positions are 1,2,3.

    # For position 1 (x=1): binary of 0 (x-1) is '00' (with 2 bits) -> number of 1s is 0 -> even -> mountain? 
    # For position 2 (x=2): binary of 1 is '01' -> 1 -> odd -> valley?
    # For position 3 (x=3): binary of 2 is '10' -> 1 -> odd -> valley.

    # Then, the sequence of creases (for positions 1,2,3) is: mountain, valley, valley.

    # But the sample input says there is a contiguous subsequence "MMVM". Wait, that's 4 creases. 

    # Actually, the sample input has N=4, so we are looking at 4 consecutive creases. 

    # Let me consider the entire