class Solution:
    def smallestString(self, s: str) -> str:
        ct1 = 0
        for ch in s:
            if ch == 'a':
                ct1 += 1
            else:
                break
        ans = 'a' * ct1
        s = s[ct1:]  # remaining string after leading a's

        if not s:
            return ans[:-1] + 'z'

        change = False
        contiguous = True
        ct2 = 0

        for i, ch in enumerate(s):
            ct2 = i + 1
            if ch != 'a':
                ans += chr(ord(ch) - 1)
                change = True
                continue
            else:
                ans += ch
                if change:
                    contiguous = False
            if not contiguous:
                break

        return ans + s[ct2:]