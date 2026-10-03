class Solution:
    def numPermsDISequence(self, s: str) -> int:
        n = len(s) + 1
        mod = 10**9 + 7
        
        # We'll use dynamic programming with state (i, last) where i is the position and last is the last digit chosen.
        # But the range of digits is 0 to 9, and the sequence length is n (which can be up to 10, since s length is up to 9).
        # However, the state space is (n, 10) which is 100 states, so we can do DP.
        # Alternatively, we can use combinatorial DP.

        # Another known approach: 
        #   Let dp[i][j] = number of ways to form a sequence of length i+1 ending with digit j (where j from 0 to 9) and satisfying the pattern up to index i.
        #   But note: the pattern is given by s, and the sequence must be strictly increasing? Actually, the pattern defines the relation between consecutive digits.

        # However, note: the problem does not require the entire sequence to be strictly increasing, only the consecutive relations.

        # But the example: s="I" -> 10, s="D" -> 1.

        # Let's try a combinatorial DP:

        # We can think of the sequence as being built by inserting either increasing or decreasing. The known solution for "DI String Match" is to use a greedy method, but here we are counting.

        # Alternatively, we can use a DP that considers the positions and the last digit.

        # But note: the digits are from 0 to 9, and the sequence length is n (which is at most 10). We can use DP with state (i, last) where i is the position (0-indexed) and last is the last digit (0-9). But we must avoid using the same digit twice? 

        # Actually, the problem does not specify distinct digits, but the pattern requires that consecutive digits are different (since one is greater and the other is less). However, the entire sequence might have repeated digits? 

        # But the example s="I": 
        #   The code returns 10, which is the number of digits (0-9) for the first position, and then the second digit must be greater than the first. But if we allow repetition, then for the first digit 0, the second digit can be 0,1,...,9 (10 ways) but then the pattern requires strictly increasing? Actually, the pattern requires strictly increasing for 'I', so the second digit must be greater than the first. So for first digit 0, second digit can be 1-9 (9 ways). Similarly, for first digit 1, second digit 2-9 (8 ways) ... for first digit 8, second digit 9 (1 way) and first digit 9: 0 ways. Total: 9+8+...+1 = 45, but the code returns 10.

        # The code returns 10 for s="I", so the problem must be counting something else.

        # Let me read the problem statement again (from the code's context): 
        #   "Given a string s of length n-1 containing only characters 'D' and 'I', and a digit sequence of length n, return the number of strictly increasing digit sequences (each digit from 0 to 9) of length n that satisfy the pattern."

        # But wait, the problem says "strictly increasing digit sequences", so the entire sequence must be strictly increasing. Then the pattern must be all 'I's? 

        # However, the example s="D" returns 1. 

        # This is confusing.

        # After checking, the problem is from LeetCode: "Number of Ways to Form a Strictly Increasing Digit Sequence" with a pattern. 

        # Actually, the problem is: 
        #   We are to form a sequence of length n (n = len(s)+1) using digits from 0 to 9, and the sequence must be strictly increasing (so distinct digits and increasing) and satisfy the pattern.

        # But then, for s="I", the pattern requires that the sequence is strictly increasing (which is already satisfied by the entire sequence being strictly increasing) and the pattern is just a string of 'I's. But wait, the pattern is given for consecutive digits. In a strictly increasing sequence, every consecutive pair is increasing, so the pattern must be all 'I's. 

        # However, the example s="D" returns 1. 

        # This indicates that the problem does not require the entire sequence to be strictly increasing, but only the consecutive relations as given by the pattern.

        # But then,