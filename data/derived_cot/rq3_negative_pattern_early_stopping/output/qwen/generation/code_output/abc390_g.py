def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    
    # Precompute the number of digits for each number from 1 to N
    # But we don't need each individually, we need the total length and the distribution of lengths.
    # Actually, we need to know the length of each number from 1 to N.
    # We can precompute an array `digits` where digits[i] is the number of digits of i.
    # But N can be up to 200000, so we can compute the length for each number by converting to string, but that might be slow.
    # Alternatively, we can use logarithms or math, but that might be overkill.
    # We can also precompute the total length T = sum_{i=1}^{N} (floor(log10(i)) + 1)
    # But we need more than that: we need to know, for each number, its length, and then use that to compute the contribution.

    # However, note: the problem is to sum over all permutations. We can use the idea of linearity of summation and consider the contribution of each number in each position.

    # Let F = total sum over all permutations.
    # We can break F as the sum over each position j (from 0 to N-1) of the sum of the contributions of each number placed at position j.

    # But the contribution of a number x placed at position j is:
    #   x * (10 raised to the total length of the numbers that come after it) 

    # However, the total length of the numbers that come after it depends on the permutation. But note: the set of numbers is fixed, so the total length of the remaining numbers is fixed for a given set of numbers that are not chosen. But wait, the permutation is over all numbers, so when we fix a number at position j, the remaining numbers are all the other numbers, and the total length of the remaining numbers is T - (length of x). But wait, no: the remaining numbers are the other N-1 numbers, so the total length of the remaining numbers is T - (length of x). However, the exponent is the total length of the remaining numbers (because the remaining numbers are concatenated after x, so they form the lower digits). 

    # But wait, the entire number is built by concatenation. The value contributed by x is x * (10^(total_length_of_remaining_numbers)). 

    # However, note: the remaining numbers are not necessarily in a fixed order, but the total length is fixed (T - len(x)), so the exponent is fixed for a given x and the set of remaining numbers. 

    # But wait, the set of remaining numbers is fixed (all numbers except x) so the total length of the remaining numbers is fixed (T - len(x)). Therefore, the contribution of x when placed at a position is x * (10^(T - len(x))).

    # Now, how many times does x appear at a position? 

    # Actually, we can use the following:

    # The total sum F = sum_{permutation P} f(P)

    # We can also think: for each number x, how many times does it appear in a position where the total length of the remaining numbers is (T - len(x))? 

    # Actually, in every permutation, each number x appears exactly (N-1)! times. But wait, no: in a permutation of N elements, each element appears in each position exactly (N-1)! times. 

    # However, the exponent (the power of 10) depends on the position. But note: the exponent is determined by the total length of the numbers that are placed after x. 

    # But wait, the position in the permutation does not directly determine the exponent. The exponent is determined by the total length of the numbers that are placed after x. 

    # However, the set of numbers that are placed after x is fixed (all numbers except x) and the total length is T - len(x). But wait, that is independent of the order of the remaining numbers. 

    # Therefore, the contribution of x is: x * (10^(T - len(x))) * (number of permutations where x is placed at a position and the remaining numbers are arranged arbitrarily). 

    # But note: the position of x in the permutation does not matter for the exponent because the exponent is the total length of the numbers that come after x, which is always T - len(x) (since the set of remaining numbers is fixed). 

    # However, wait: the exponent is the total length of the numbers that come after x, which is indeed T - len(x) (