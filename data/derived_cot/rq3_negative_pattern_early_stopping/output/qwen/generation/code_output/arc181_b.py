import sys

def main():
    data = sys.stdin.read().splitlines()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        S = data[index]; index += 1
        X = data[index]; index += 1
        Y = data[index]; index += 1
        
        n0_x = X.count('0')
        n1_x = X.count('1')
        n0_y = Y.count('0')
        n1_y = Y.count('1')
        
        # If the total number of S blocks in X and Y are the same, then we can set T to empty and check if the strings are equal.
        # But note: if n0_x == n0_y, then the two strings are both S repeated n0_x times (if T is empty) and then they are equal.
        # However, what if n0_x != n0_y? Then we must have T non-empty and the equation (n0_x - n0_y)*len(S) = (n1_y - n1_x)*len(T) must hold.

        # But note: the equation must hold for the length. However, the string equality is more than length.

        # Let's consider: the entire string from X is built by replacing each '0' by S and each '1' by T.
        # Similarly for Y.

        # We can also note: the entire string from X must be equal to the entire string from Y.

        # Let L = len(S)
        # The length of the string from X is: n0_x * L + n1_x * len_T
        # The length of the string from Y is: n0_y * L + n1_y * len_T

        # So: n0_x * L + n1_x * len_T = n0_y * L + n1_y * len_T
        # => (n0_x - n0_y) * L = (n1_y - n1_x) * len_T

        # But note: the equation must hold. However, we don't know len_T. But note: the entire string must be the same.

        # However, there is a catch: the two strings are built by the same T. But the order of blocks is different.

        # We can also consider: the string from X must be the same as the string from Y. Therefore, the two strings must have the same pattern of S and T.

        # But note: the pattern is given by X and Y. The two strings are built by two different orders of S and T.

        # However, we can break down the string from X and Y into segments. But note: the string T is arbitrary, so we can choose T to be a string that fits the pattern.

        # Actually, we can think of the entire string from X as a sequence of blocks (each block is either S or T). Similarly for Y.

        # The condition for the two strings to be equal is that they are the same string. Therefore, the two sequences of blocks must be the same? Not necessarily, because T is arbitrary and S is fixed.

        # But note: the blocks are either S or T. So the entire string is a concatenation of S and T. However, the order of blocks is fixed by X and Y.

        # We can compare the two strings by comparing the blocks at the same positions? But the lengths of the blocks are fixed by S and T.

        # However, note: the equation above must hold for the total length. But even if the total length is the same, the strings might not be equal.

        # Example: S = "ab", X = "0", Y = "1", then we require T such that "ab" = T. Then T must be "ab". Then the equation: 1*2 + 0*2 = 0*2 + 1*2 -> 2 = 2, which holds. But then the strings are "ab" and "ab", so it works.

        # Another example: S = "ab", X = "00", Y = "11", then we require T such that "abab" = T+T. Then T must be "abab" (if we set T="abab", then the string from X is "abab", and from Y is "abababab", which is not equal). Actually, wait: the equation: 2*2 + 2*len_T = 0*2 + 2*len_T -> 4 + 2*len_T = 2*len_T -> 4=0, which is impossible. So no solution.

        # Actually, the equation is: (n0_x - n0_y)*L = (n1_y - n1_x)*len_T.

        #