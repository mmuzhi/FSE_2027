class Solution:
    def numPermsDISequence(self, s: str) -> int:
        n = len(s) + 1
        mod = 10**9 + 7
        
        # dp[i][j] = number of ways to have built a sequence of length i (i from 0 to n) 
        # with the last element being the j-th smallest among the i elements (j from 0 to i)
        dp = [[0] * (n) for _ in range(n+1)]
        
        # Base case: sequence of length 0, there is 1 way (empty sequence)
        dp[0][0] = 1
        
        for i in range(n):
            # i is the current length (from 0 to n-1), and we are going to extend to i+1
            for j in range(i+1):
                if dp[i][j] == 0:
                    continue
                # The next character is s[i]
                if s[i] == 'I':
                    # We must choose a number greater than the last one.
                    # In the set of i+1 elements, the last element is the j-th smallest, so there are (i - j) numbers greater than it.
                    # But note: we are going to choose the next number from the remaining n - i - 1 numbers? 
                    # Actually, we are building the sequence by inserting the next number. The next number must be greater than the last one, so it must be one of the numbers that are not among the j+1 smallest (because the last element is the j-th smallest, so there are j elements less than it, and the next number must be greater, so it must be chosen from the remaining (n - i - 1) numbers that are greater than the last one? But wait, we don't know the actual numbers.

                    # Alternatively, we can use the idea of "relative ordering": 
                    # The next number must be greater than the last one, so in the set of i+1 numbers, the last one is the j-th smallest, so there are (i+1 - 1 - j) = i - j numbers greater than it. But we are going to choose one number from the remaining n - i - 1 numbers? 

                    # Actually, we are building the sequence by inserting the next number. The next number must be greater than the last one, so it must be chosen from the numbers that are greater than the last one. But note: we are not fixing the set of numbers, so we can use the combinatorial count.

                    # However, note: the sequence must be a permutation of n distinct numbers. We are building it step by step.

                    # Let's change our state definition: 
                    # We are going to use dp[i][j] = number of ways to have built a sequence of length i (so we have used i numbers) and the last element is the j-th smallest among the i numbers.

                    # Then, for the next element (if it is 'I'), we must choose a number that is greater than the last one. 
                    # In the set of i numbers, the last one is the j-th smallest, so there are j numbers less than it and (i - j - 1) numbers greater than it? 
                    # But wait, we are going to choose the next number from the remaining n - i numbers. However, the condition is only about the relative order.

                    # Actually, we can use the following: 
                    # The next number must be greater than the last one, so it must be chosen from the numbers that are greater than the last one. But note: the entire sequence must be a permutation of n distinct numbers, so we are free to choose any number that hasn't been used and satisfies the condition.

                    # But note: the condition is only about the immediate next element. 

                    # We can use the following combinatorial count: 
                    # The next number must be greater than the last one, so we have (n - i - 1) numbers left, and we must choose one that is greater than the last one. But we don't know the actual numbers, so we can use the relative ordering.

                    # Alternatively, we can use a different state: 
                    # Let dp[i][j] = number of ways to have built a sequence of length i (so we have i elements) and the last element is the j-th smallest among the i elements.

                    # Then, for the next element (if 'I'), we must choose a number that is greater than the last one. In the set of i+1 elements, the last one is the j-th smallest, so there are (i+1 - 1 - j) = i - j numbers greater than it. But we are going to choose one number from the remaining n - i numbers