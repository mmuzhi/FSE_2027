class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute combinations for n up to 1000 (x up to 1000)
        max_n = 1000
        comb = [[0]*(max_n+1) for _ in range(max_n+1)]
        for i in range(max_n+1):
            comb[i][0] = 1
            for j in range(1, i+1):
                comb[i][j] = (comb[i-1][j] + comb[i-1][j-1]) % MOD
        
        # Precompute powers for base up to 1000 and exponent up to 1000
        # But we can use pow with modulus for each k and base i (for inclusion-exclusion)
        # Alternatively, use DP for surjective functions
        # But note: n and x are up to 1000, so we can iterate k from 0 to min(n, x)
        # For each k, we need to compute the number of surjective functions from n to k, which is:
        #   S(n, k) = (1/k!) * sum_{i=0}^{k} (-1)^i * C(k, i) * (k-i)^n
        # But actually, the inclusion-exclusion formula for surjective functions is:
        #   F(n, k) = sum_{i=0}^{k} (-1)^i * C(k, i) * (k-i)^n
        # Then, the number of ways to have exactly k non-empty stages is: C(x, k) * F(n, k)
        # Then, the total ways is: sum_{k=0}^{min(n, x)} [ C(x, k) * F(n, k) * (y^k) ]
        # But wait, note: the score assignment is y^k (each of the k bands gets a score from 1 to y). 

        # However, note: the problem allows stages to be empty. So k can be from 0 to min(n, x). But actually, k can be from 0 to x (if x <= n, then k from 0 to x; if x > n, then k from 0 to n). 

        # We'll iterate k from 0 to min(n, x) (since if k > n, then it's impossible to have k non-empty stages with n performers).

        # But note: the inclusion-exclusion formula for surjective functions requires that k <= n. So we only consider k from 0 to min(n, x).

        # Steps:
        # 1. Precompute combinations up to max_n (1000) for C(x, k) and for the inclusion-exclusion part (C(k, i)).
        # 2. For each k from 0 to min(n, x):
        #   a. Compute F(n, k) = sum_{i=0}^{k} (-1)^i * C(k, i) * (k-i)^n
        #   b. Then, ways_k = C(x, k) * F(n, k) * (y^k)
        # 3. Sum all ways_k and take modulo MOD.

        # But note: the inclusion-exclusion formula for surjective functions is correct.

        # However, note: the problem does not require that the bands are formed only from non-empty stages. The assignment of performers is independent, and then the score assignment is for each non-empty stage. 

        # But wait, the above formula counts the number of ways to assign n distinguishable performers to k distinguishable stages (with no stage empty). Then, we choose k stages from x (C(x, k)), and then assign the performers to these k stages (F(n, k)). 

        # But actually, the assignment of performers to stages is: each performer chooses one of x stages. The condition is that exactly k stages are non-empty. 

        # The total number of ways to assign n distinguishable performers to x stages (without the surjective condition) is x^n. 

        # The number of ways to have exactly k non-empty stages is: 
        #   C(x, k) * (number of surjective functions from n to k)
        # which is exactly C(x, k) * F(n, k)

        # Then, for each such assignment, we assign a score to each of the k bands (non-empty stages): y^k ways.

        # So, the total ways is: 
        #   Sum_{k=0}^{min(n, x)} [ C(x, k) * F(n, k) * (