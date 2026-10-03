class Solution:
    def hasMatch(self, s: str, p: str) -> bool:
        if '*' not in p:
            return False
        index_star = p.index('*')
        left_part = p[:index_star]
        right_part = p[index_star+1:]
        n = len(s)
        m_left = len(left_part)
        m_right = len(right_part)
        # If the pattern is just '*' then left and right are empty, so we need a substring that is non-empty and matches the pattern (empty string) which is not allowed. So return false.
        # But actually, the pattern is the empty string, which is not a substring (non-empty required). So we can handle by checking the length condition.
        # We'll iterate over all starting indices and all ending indices that are at least m_left + m_right - 1 away.
        # But note: the substring must be at least m_left + m_right long.
        # However, if m_left + m_right is 0 (i.e., both left and right are empty), then the pattern is just '*' and we are looking for an empty substring, which is not allowed. So we can skip that case.
        # Actually, we can handle it by the loop: if m_left + m_right == 0, then the pattern is just '*' and we need a substring of length 0, which is not allowed. So we return false.
        # But the problem says p contains exactly one '*', so p is at least 1 character. But if p is "*", then left and right are empty, and the substring must be non-empty, so no match.
        # So we can simply check: if m_left + m_right == 0, then return False.
        if m_left + m_right == 0:
            return False
        # Iterate over all starting indices
        for i in range(n):
            # The substring must start with left_part
            if s[i:i+m_left] != left_part:
                continue
            # The substring must end with right_part
            # We need to find a j such that the substring from i to j ends with right_part and has length at least m_left + m_right
            # The minimal j is i + m_left + m_right - 1
            # But we can also have longer substrings
            # We'll iterate j from i + m_left + m_right - 1 to n-1
            # But note: the substring must end with right_part, so the last m_right characters must be right_part.
            # So j must be at least i + m_left + m_right - 1, and the substring from j - m_right + 1 to j+1 must be right_part.
            # Actually, the substring from i to j must have the last m_right characters equal to right_part.
            # So j must be at least i + m_left + m_right - 1, and the last m_right characters are from j - m_right + 1 to j.
            # We can set j from i + m_left + m_right - 1 to n-1, but we can also break early if the substring is too long? But n is small.
            # Alternatively, we can set j from i + m_left + m_right - 1 to n-1, but we can also consider that the substring must end at or after i + m_left + m_right - 1.
            # But we can also consider that the substring must end with right_part, so we can set j from max(i + m_left + m_right - 1, i + m_left - 1 + m_right) to n-1, but actually, the minimal j is i + m_left + m_right - 1.
            # But note: the substring must be at least m_left + m_right long, so j must be at least i + m_left + m_right - 1.
            # Now, for each j from i + m_left + m_right - 1 to n-1, check if the substring from j - m_right + 1 to j+1 is right_part.
            # But wait, the substring from i to j must end with right_part, so the last m_right characters are s[j - m_right + 1: j+1] (if we consider 0-indexed, then from j - m_right + 1 to j inclusive). But if j - m_right + 1 is less than i, then it's not valid. Actually, the substring from i to j must have the last m_right characters equal to right_part, so the part from j - m_right + 1 to j must be within the substring, i.e., j - m_right + 1 must be >= i. But since j is at least i + m_left + m_right - 1, then j - m_right + 1 is