class Solution:
    def minOperations(self, n: int, m: int) -> int:
        # Check if n or m is prime
        def is_prime(x):
            if x < 2:
                return False
            for i in range(2, int(x**0.5) + 1):
                if x % i == 0:
                    return False
            return True
        
        if is_prime(n) or is_prime(m):
            return -1
        
        # If n equals m, then cost is n (only one state)
        if n == m:
            return n
        
        # We'll use Dijkstra's algorithm where the state is the current number
        # The graph: from a number, we can change each digit (if allowed) to get a new number
        # The cost is the sum of the numbers we've visited so far (including the current)
        # But note: the cost is the sum of all values that n takes, so we are accumulating the cost as we traverse the path.
        # We want to minimize the total cost to reach m.
        # We can use a priority queue (min-heap) where the priority is the total cost so far.
        # But note: the cost is the sum of the numbers, and we are visiting states (numbers). However, the same number might be reached by different paths with different total costs.
        # We need to keep track of the minimum total cost to reach a number.
        # But the state space is numbers with the same number of digits as n (and m). We can represent the number as an integer.
        # The operations: for each digit in the number, we can increase it (if not 9) or decrease it (if not 0) by 1, and then form a new number.
        # But note: the entire number must be composite (non-prime) for the new state.
        # We'll use a dictionary (or list) to store the best (minimum) total cost to reach a number.
        # However, the state space is 9000 for 4-digit numbers, which is acceptable.
        # But note: the numbers must have the same number of digits as n (and m). So, we cannot have leading zeros. But the input n and m have the same number of digits, so we are only considering numbers with that many digits (unless we change the number of digits? Actually, the operations are on digits, but if we decrease a digit and it becomes 0, then the number of digits remains the same (unless the number is like 1000, and we decrease the first digit to 0, then it becomes 0000, which is 0, but 0 is not positive and the problem says n, m >=1). But the problem states that n and m are at least 1, and have the same number of digits. So, we must maintain the same number of digits. Therefore, we cannot have leading zeros. So, the first digit cannot be 0. But in the operations, if we decrease the first digit and it becomes 0, then the number would have fewer digits, which is not allowed. So, we must avoid that. Therefore, when decreasing the first digit, we must ensure that the new digit is not 0 (or if it becomes 0, then the number would have fewer digits, which is not allowed). But wait, the problem says "n and m consist of the same number of digits", so we must stay in the same digit length. Therefore, we cannot decrease the first digit to 0 because that would change the number of digits. Similarly, we cannot increase the last digit to 10, which would change the number of digits. So, the operations are only allowed if the resulting number has the same number of digits. Therefore, for the first digit, we cannot decrease it to 0 (because then the number would have one less digit). Similarly, for the last digit, we cannot increase it to 10 (which would require a new digit). So, the operations are constrained by the digit position and the fact that the number must have the same number of digits.

        # Actually, the problem does not explicitly say that the number must retain the same number of digits, but the inputs n and m have the same number of digits, and the operations are defined on the digits of n. But if we change a digit and the number of digits changes, then we are effectively changing the number of digits, which is not allowed because n and m have the same number of digits. So, we must ensure that the operations do not change the number of digits. Therefore, for the first digit, we cannot decrease it to 0 (because then the number would have one less digit). Similarly, for the last digit, we cannot increase it to 10 (which would require a carry, but then the number of