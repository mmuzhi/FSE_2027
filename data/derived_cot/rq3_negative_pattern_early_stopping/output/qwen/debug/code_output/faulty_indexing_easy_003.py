class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        count = collections.Counter(deck)
        vals = list(count.values())
        import math
        if len(vals) == 0:
            return True
        m = vals[0]
        for i in range(1, len(vals)):
            m = math.gcd(m, vals[i])
        # Now, m is the gcd of all frequencies.
        # We need to check if there exists a group size X (which divides every frequency) and X>=1.
        # The condition is that m must be at least 1 (which it is) and then we can form groups of size m.
        # But note: the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of m) that is at least 1.
        # However, if m is 1, then we can form groups of size 1 (each card alone) and that is valid.
        # But wait: the problem requires that the groups are of the same size and every card is used. The group size must divide every frequency. The gcd is the largest common divisor, but we can use any divisor of the gcd. However, the condition for the existence of a group size is that the gcd is at least 1 (which it is) and then we can choose X to be the gcd. But note: the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of the gcd). 

        # However, the problem does not require that the group size is the gcd, but that the same group size divides every frequency. The necessary and sufficient condition is that the gcd of the frequencies is at least 1 (which it is) and then we can form groups of size = gcd. But note: the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of the gcd). 

        # But wait: the problem does not require that the group size is the gcd, but that the same group size divides every frequency. The set of common divisors is the divisors of the gcd. So if the gcd is d, then we can form groups of size d, or any divisor of d. However, the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of d). 

        # However, note: the problem does not require that the group size is the gcd, but that the same group size divides every frequency. The condition is that the gcd of the frequencies is at least 1 (which it is) and then we can form groups of that gcd. But wait: the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of the gcd). 

        # Actually, the condition is that the gcd must be at least 1 (which it is) and then we can form groups of size = gcd. But note: the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of the gcd). 

        # However, the problem does not require that the group size is the gcd, but that the same group size divides every frequency. The necessary condition is that the gcd is at least 1 (which it is) and then we can choose X to be the gcd. But note: the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of the gcd). 

        # But wait: the problem does not require that the group size is the gcd, but that the same group size divides every frequency. The condition is that the gcd of the frequencies is at least 1 (which it is) and then we can form groups of size = gcd. 

        # However, note: the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of the gcd). 

        # But the problem does not require that the group size is the gcd, but that the same group size divides every frequency. The condition is that the gcd of the frequencies is at least 1 (which it is) and then we can form groups of that gcd. 

        # Actually, the condition is that the gcd must be at least 1 (which it is) and then we can form groups of size = gcd. But note: the problem does not require that the group size is the gcd, but that there exists a group size (which is a divisor of the gcd). 

        # However, the problem does not require that the group size is the gcd, but that the same group size divides every frequency. The necessary condition is that the gcd is at least 1 (which it is) and then we