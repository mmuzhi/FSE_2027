class Solution:
    def areAlmostEqual(self, s1: str, s2: str) -> bool:
        if len(s1) != len(s2):
            return False
        if s1 == s2:
            return True
        
        diff = []
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                diff.append((s1[i], s2[i]))
                if len(diff) > 2:
                    return False
        
        if len(diff) == 0:
            return True
        elif len(diff) == 2:
            # Check if the two differences are reverses of each other
            a, b = diff[0]
            c, d = diff[1]
            return (a == d and b == c)
        else:
            return False