class Solution:
    def areAlmostEqual(self, s1: str, s2: str) -> bool:
        if len(s1) != len(s2):
            return False

        diff = []
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                diff.append([s1[i], s2[i]])

        return len(diff) == 0 or (len(diff) == 2 and diff[0] == diff[1][::-1])