class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        L = len(s2)
        nxt = [0] * L
        add = [0] * L

        for p in range(L):
            q = p
            cnt = 0
            for ch in s1:
                if ch == s2[q]:
                    q += 1
                    if q == L:
                        cnt += 1
                        q = 0
            nxt[p] = q
            add[p] = cnt

        seen = {}
        p = 0
        cnt = 0
        i = 0

        while i < n1:
            if p in seen:
                start_i, start_cnt = seen[p]
                cycle_len = i - start_i
                cycle_cnt = cnt - start_cnt
                blocks_left = n1 - start_i

                cnt = start_cnt + (blocks_left // cycle_len) * cycle_cnt
                rem = blocks_left % cycle_len

                q = p
                for _ in range(rem):
                    cnt += add[q]
                    q = nxt[q]

                return cnt // n2

            seen[p] = (i, cnt)
            cnt += add[p]
            p = nxt[p]
            i += 1

        return cnt // n2