from typing import List

class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def kth(self, k: int) -> int:
        idx = 0
        bit_mask = 1 << (self.n.bit_length() - 1)

        while bit_mask:
            nxt = idx + bit_mask
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            bit_mask >>= 1

        return idx + 1


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        if not nums or k <= 0:
            return []

        vals = sorted(set(nums))
        pos = {v: i + 1 for i, v in enumerate(vals)}

        tree = FenwickTree(len(vals))
        ans = []

        for i, x in enumerate(nums):
            tree.add(pos[x], 1)

            if i >= k:
                tree.add(pos[nums[i - k]], -1)

            if i >= k - 1:
                if k & 1:
                    ans.append(float(vals[tree.kth(k // 2 + 1) - 1]))
                else:
                    left = vals[tree.kth(k // 2) - 1]
                    right = vals[tree.kth(k // 2 + 1) - 1]
                    ans.append((left + right) / 2.0)

        return ans