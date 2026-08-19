class Solution:
    def palindromePartition(self, s: str, k: int) -> int:

        # This is the cost function
        def Cost(s):
            i, j, c = 0, len(s) - 1, 0
            while i < j:
                if s[i] != s[j]:
                    c += 1
                j -= 1
                i += 1
            return c

        dp = {}

        # Recursion
        def A(s, k):
            # Memoization
            if (s, k) in dp:
                return dp[(s, k)]
            # if k==1 then we want the whole string, there is no other way
            if k == 1:
                return Cost(s)

            # initial value to max
            f = float('inf')

            # start checking whole string
            for x in range(1, len(s) + 1):
                # check whether both strings exist
                if len(s[:x]) and len(s[x:]):
                    # if they exist, find the cost recursively and assign min value
                    f = min(f, Cost(s[:x]) + A(s[x:], k - 1))
            # store the min value
            dp[(s, k)] = f
            return dp[(s, k)]

        return A(s, k)