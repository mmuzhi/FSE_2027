class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        # We need to compute the minimum operations for each query [l, r]
        # Observation: Each operation reduces two numbers. But the reduction is by dividing by 4.
        # The key is to note that the total number of operations is determined by the total number of divisions by 4 needed for all numbers, but we can combine operations.

        # Actually, think of it as: each number x requires a certain number of operations to be reduced to 0. But note, one operation can handle two numbers.

        # However, note that the operation is defined as: take two numbers and replace them with floor(a/4) and floor(b/4). This is equivalent to reducing two numbers by one level in their division by 4.

        # Let's define for each number x, the number of operations it must undergo is the number of times we need to divide it by 4 (taking floor) until it becomes 0. But note, we can combine operations.

        # Actually, the problem is similar to: we have a set of numbers, and each operation reduces two numbers by a factor of 4 (i.e., we are effectively reducing the "depth" of the number in base 4). 

        # But note: the operation doesn't necessarily have to be on two numbers that are being reduced at the same time. We can use the same number multiple times? Actually, no, because once a number is replaced, it's gone. But wait, the operation replaces two numbers with two new numbers. So, the array size remains the same until the numbers become 0.

        # Actually, the operation replaces two numbers with two new numbers. So, the array size is constant until zeros appear. But zeros can be left and not used in operations.

        # However, the problem is asking for the minimum number of operations to reduce all to zero.

        # Let me try to derive a formula.

        # Consider a single number x. How many operations are needed to reduce it to 0? Actually, we can't reduce a single number without another number. But note, we can combine operations.

        # Alternatively, think in terms of the total number of divisions by 4 that must be performed. Each operation provides two divisions (because it divides two numbers). But wait, no: each operation divides two numbers by 4, so it's two divisions. But the same number might be divided multiple times.

        # Actually, the total number of divisions by 4 required is the sum over all numbers of the number of times we need to divide that number by 4 until it becomes 0. But note, we can do two divisions at once in one operation.

        # However, the catch is that we can only operate on two numbers at a time, and the numbers are being reduced in a way that might interleave.

        # Another perspective: each number x can be represented in base 4. The number of operations needed for x is the number of digits in its base 4 representation? Not exactly.

        # Let me consider the process for a single number x. To reduce x to 0, we need to perform a series of divisions by 4. But each operation can only handle two numbers. So, if we have n numbers, the total number of operations is at least ceil(total_divisions / 2). But wait, the divisions are happening on different numbers and the same number might be divided multiple times.

        # Actually, the problem is equivalent to: we have a multiset of numbers. Each operation: pick two numbers, and replace each by floor(number/4). We want to minimize the number of operations until all are 0.

        # This is similar to a problem where we have a set of coins and we can combine two coins to get two coins of a lower denomination (like a currency conversion). 

        # Let me define for each number x, the number of operations it must be part of is the number of times we need to divide it by 4 until it becomes 0. But note, one operation involves two numbers. So, the total operations is the maximum over the number of operations needed for each number? No, because we can interleave.

        # Actually, the total number of operations is the sum of the number of divisions for each number divided by 2 (ceiling) but that doesn't hold because operations are simultaneous.

        # Let me try with a small example: [2,3,4]

        # Operation 1: take 2 and 4 -> becomes 0 and 1. Now array is [0,3,1]. Then operation 2: take 3 and 1 -> becomes 0 and 0. So total 2 operations.

        # Now, for 2: it took 1 operation (because 2/4=0). For 3: 3/4=