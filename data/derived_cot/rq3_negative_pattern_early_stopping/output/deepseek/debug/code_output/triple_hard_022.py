from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in set(s2))

        rec = [0]
        track = defaultdict(int)

        cnt1 = 0          # total full s1 repetitions consumed so far
        pos = 0           # current index in s1 (0‑based)
        processed = 0     # number of s2 repetitions processed

        while True:
            for ch in s2:
                idx = s1.find(ch, pos)
                if idx == -1:
                    cnt1 += 1
                    idx = s1.find(ch)
                pos = idx + 1

            processed += 1
            rec.append(cnt1)   # total s1 repetitions used after this s2

            total_used = cnt1 + (1 if pos > 0 else 0)
            if total_used > n1:
                break

            if pos not in track:
                track[pos] = processed
            else:
                break

        if pos not in track or total_used > n1:
            cnt1 = 0
            pos = 0
            ans = 0
            for _ in range(n1):
                start = pos
                for ch in s2:
                    idx = s1.find(ch, pos)
                    if idx == -1:
                        break
                    pos = idx + 1
                else:
                    ans += 1
                    continue
                pos = 0
                cnt1 += 1
                if cnt1 >= n1:
                    break
            return ans // n2

        cycle_start_idx = track[pos]          # index in rec where the cycle starts
        before_cycle = rec[cycle_start_idx]   # s1 repetitions used before cycle
        cycle_s1 = rec[-1] - before_cycle     # s1 repetitions in one cycle
        cycle_s2 = processed - cycle_start_idx  # s2 repetitions in one cycle

        rest = n1 - before_cycle
        cycles = rest // cycle_s1             # full cycles that fit
        remain_s1 = rest % cycle_s1           # leftover s1 repetitions after cycles

        total_s2 = cycle_start_idx + cycles * cycle_s2

        cnt1 = 0
        pos = 0
        processed_tmp = 0
        for _ in range(cycle_start_idx):
            for ch in s2:
                idx = s1.find(ch, pos)
                if idx == -1:
                    cnt1 += 1
                    idx = s1.find(ch)
                pos = idx + 1
            processed_tmp += 1
            rec.append(cnt1)

        cnt1 = rec[cycle_start_idx]  # current s1 count
        for _ in range(remain_s1):
            for ch in s2:
                idx = s1.find(ch, pos)
                if idx == -1:
                    cnt1 += 1
                    idx = s1.find(ch)
                if cnt1 > n1:
                    break
                pos = idx + 1
            else:
                total_s2 += 1
                continue
            break

        return total_s2 // n2