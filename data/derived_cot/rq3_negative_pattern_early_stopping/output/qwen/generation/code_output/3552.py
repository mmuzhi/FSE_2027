class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        if n == 1:
            # For 1-digit numbers, the largest k-palindromic is the largest digit divisible by k.
            # But note: the largest digit is 9, but if 9 % k != 0, then we need to find the next largest.
            # However, the problem says for n=1, k=4, output is "8". So we need to find the largest digit (from 9 down to 0) that is divisible by k and not leading zero (but 1-digit, so no leading zero issue).
            # But note: the number must be divisible by k and be a palindrome (which 1-digit numbers are).
            # So, we can iterate from 9 down to 0 and return the first digit that is divisible by k.
            for digit in range(9, -1, -1):
                if digit % k == 0:
                    return str(digit)
            return "0"
        
        m = (n + 1) // 2
        # Start with the largest left part: '9'*m
        left_str = '9' * m
        
        # Function to form the full palindrome from left_str
        def form_palindrome(s):
            if n % 2 == 0:
                return s + s[::-1]
            else:
                return s + s[-2::-1]
        
        # Function to compute the modulus of the full palindrome from left_str without building the entire number (to avoid large integers)
        def compute_mod(s, k):
            # We can compute the modulus by processing the entire string representation of the palindrome.
            # But the string is too long, so we use modular arithmetic with the string.
            mod = 0
            for char in form_palindrome(s):
                mod = (mod * 10 + int(char)) % k
            return mod
        
        # Check the largest candidate
        mod_val = compute_mod(left_str, k)
        if mod_val == 0:
            return form_palindrome(left_str)
        
        # We need to find the largest left_str (as a number) less than the initial '9'*m such that the palindrome is divisible by k.
        # We'll convert left_str to a list of digits and decrement from the least significant digit.
        # But note: the left_str must not have leading zeros. So the first digit must be at least 1.
        # We'll start from the initial left_str and go downwards until we find a candidate.
        # However, the initial left_str is '9'*m, so we can decrement the last digit, then if that becomes 0, carry over, etc.
        # But the range is huge, so we need to be smart.

        # Alternatively, we can compute the modulus of the initial candidate and then adjust.

        # But note: the modulus of the entire number is determined by the left_str. We can compute the modulus of the initial candidate and then adjust the left_str until the modulus becomes 0.

        # We can represent left_str as a number and then subtract until we find a candidate that is divisible by k. But the number is too big.

        # Instead, we can use the following: 
        # Let candidate = int(left_str)  (but left_str is a string of m 9's, which is a big number, but m is up to 50000, so we cannot convert to int)
        # So we need to work with strings.

        # We can try to find the largest left_str (as a string) such that the modulus of the palindrome is 0.

        # We can compute the modulus of the initial candidate and then determine the required adjustment.

        # But note: the modulus operation is linear, but the entire number is built from the left_str and its mirror.

        # Another idea: 
        # The entire number is a palindrome. The modulus of the entire number modulo k is the same as the modulus of the left_str and the mirror part combined.

        # But without building the entire number, we can compute the modulus by processing the digits of the left_str and the mirror part.

        # However, we already have a function compute_mod that builds the entire string and then computes the modulus. But the entire string is 10^5 characters, which is acceptable in Python? 

        # Actually, 10^5 is 100,000 characters, which is acceptable in terms of memory and time for a single pass. But we might have to do multiple passes (if the initial candidate is not divisible by k, we need to try the next candidate).

        # But the next candidate is the next smaller left_str. The left_str is a number with m digits. The next candidate is left_str - 1,