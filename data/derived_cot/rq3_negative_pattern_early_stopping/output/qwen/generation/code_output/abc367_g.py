import sys
import numpy as np

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); m = int(data[1]); k = int(data[2])
    A = list(map(int, data[3:3+n]))
    
    # If m is 1, then we consider all non-empty subsequences, but note: the score is (XOR)^k for every subsequence.
    # But note: the problem says "if the length is a multiple of M", and M=1, so every non-empty subsequence is considered.
    # However, the straightforward way is too slow. We need a better method.

    # We'll use generating functions and roots of unity for the length dimension.

    # Step 1: Precompute the M-th roots of unity modulo MOD.
    # But note: M can be up to 100, and MOD is 998244353. We need to check if MOD has a primitive M-th root of unity.
    # Since MOD is 998244353, and M divides 998244352 (the order of the multiplicative group), we can use a primitive root.

    # However, we don't need the full polynomial transform for the length dimension. We need to evaluate the polynomial in y at M points (the M-th roots of unity).

    # But note: the generating function is a product over i of (1 + y * z^{A_i}), but we are treating z as a variable and y as a variable. Actually, we are interested in the coefficients for each fixed z (i.e., for each x) and then summing over y^l for l multiple of M.

    # Alternatively, we can use the following:

    # Let F(z) = [f_0, f_1, ..., f_{n}] where f_l is the generating function for the number of subsequences of length l with XOR z. But that is too big.

    # We need to use the fact that the XOR values are in the range [0, 2^20). We can use a 1D array for the XOR values and then use dynamic programming with the Fast Walsh-Hadamard Transform (FWHT) for the subset XOR, but then we have to account for the length.

    # Another idea: use the concept of "generating function" for the entire set and then use the roots of unity filter for the length.

    # We can write:
    # Let P(y) = ∏_{i=1}^{n} (1 + y * (1 + z^{A_i}))   [But this is not standard]

    # Actually, the generating function for the entire set is:
    # P(y, z) = ∏_{i=1}^{n} (1 + y * z^{A_i})

    # Then, the sum_{l ≡0 mod m} [coefficient of y^l * z^x] is (1/m) * sum_{j=0}^{m-1} P(ω^j, z) evaluated at the coefficient of z^x.

    # But note, P(y, z) is a polynomial in y and z. We can fix z and then consider P(y, z) as a polynomial in y. Then, the coefficients of y^l are the number of subsequences of length l with XOR x (for fixed x). But actually, the coefficient of y^l * z^x is the number of subsequences of length l with XOR x.

    # So, for each x, we have a polynomial Q_x(y) = P(y, z) with z fixed to x? Actually, no. The generating function is:
    # P(y, z) = ∏_{i} (1 + y * z^{A_i})
    # Then, the coefficient of z^x is the sum over all subsequences with XOR x of y^{l} (where l is the length). So, for each x, we have a polynomial in y: Q_x(y) = sum_{l} (number of subsequences of length l with XOR x) * y^l.

    # Then, the sum_{l ≡0 mod m} (number of subsequences of length l with XOR x) is the sum_{l ≡0 mod m} [coefficient of y^l in Q_x(y)].

    # And by the roots of unity filter, that is (1/m) * sum_{j=0}^{m-1} Q_x(ω^j), where ω is a primitive m-th root of unity.

    # Then, the answer is: sum_{x} [ (1/m) * sum_{j=0}^{m