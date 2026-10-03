class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        for i in range(n):
            if s[i] == '0':
                continue
            d = int(s[i])
            # We'll consider substrings ending at i, starting from j to i.
            # We need to check if the number formed by s[j:i+1] is divisible by d.
            # We can compute the number modulo d from right to left.
            # But note: the substring can have leading zeros, but that doesn't affect the modulus (since 0 mod d is 0).
            # We can use a running modulus for the substring from j to i, but we need to reset for each j.
            # Alternatively, we can compute the modulus for the substring from j to i by iterating from j to i and building the number mod d.
            # But that would be O(n^2) in worst-case (if we do for each j from 0 to i, and for each j we do a loop from j to i). Total O(n^2) which is too slow for n=10^5.

            # We need a better way.

            # Idea: Precompute for each position i, and for each divisor d (from 1 to 9) the remainder of the substring from j to i? But we don't know the divisor in advance.

            # Alternatively, we can use a different approach: iterate over divisors (digits 1-9) and then for each occurrence of that digit, count the substrings ending at that occurrence that are divisible by the digit.

            # But then we have to combine the counts for each divisor.

            # However, note: the same substring is considered only once (it has one last digit). So we can do:

            # For each divisor d (from 1 to 9), we can collect the indices where s[i] == str(d). Then for each such index i, we want to count the number of substrings ending at i (i.e., starting at j from 0 to i) such that the number formed by s[j:i+1] is divisible by d.

            # But then we have to do for each divisor d and for each occurrence i of d, and then for each j from 0 to i, check the modulus. That is still O(n^2) in the worst-case.

            # We need an efficient way to compute the modulus for the substring from j to i for a fixed d.

            # We can precompute for each divisor d a list of indices where d occurs. Then for each occurrence i (for divisor d), we want to count the number of j (0<=j<=i) such that the number formed by s[j:i+1] is divisible by d.

            # We can use a rolling hash for modulus? But the modulus base is d, and d is small (1-9). We can compute the modulus from left to right? Actually, we can compute the number mod d by:

            # Let num = 0
            # For k from j to i:
            #   num = (num * 10 + int(s[k])) % d

            # But then we have to do this for each j from 0 to i. That is O(i) per i, so worst-case O(n^2) which is 10^10 for n=10^5, which is too slow.

            # We need to optimize.

            # Another idea: use a dictionary to store the remainders for a fixed divisor d for all prefixes? But the divisor d is fixed for the current substring, and the substring is from j to i, so we need the remainder of the substring from j to i.

            # We can precompute for each divisor d a prefix array for the entire string? But the divisor d is fixed and the string is fixed, but we have 9 divisors. We can do:

            # For each divisor d (1-9), we can precompute an array rem[i] for the remainder of the substring from 0 to i (i.e., s[0:i+1]) mod d. But then how to get the remainder for substring from j to i? We can use:

            # Let F(j, i) = (F(0, j-1) * 10^(i-j+1) + (number formed by s[j:i+1])) mod d.

            # But that requires knowing the remainder of the prefix up to j-1 and the power of 10 mod d. However, note that the substring from j to i is independent of the prefix.

            # Alternatively, we can compute the remainder for the substring from j to i by:

            # Let rem = 0
            # For k from j to i:
            #   rem = (