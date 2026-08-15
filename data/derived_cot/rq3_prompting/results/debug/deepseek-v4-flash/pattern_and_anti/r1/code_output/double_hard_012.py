from typing import List

class FenwickTree:
    def __init__(self, nums: List[int]):
        self.vals = sorted(set(nums))
        self.n = len(self.vals)
        self.pos = {v: i + 1 for i, v in enumerate(self.vals)}
        self.bit = [0] * (self.n + 1)
        self.total = 0
        self.step = (1 << (self.n.bit_length() - 1)) if self.n else 0

    def insert(self, x: int) -> None:
        i = self.pos[x]
        self.total += 1
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += 1
            i += i & -i

    def remove(self, x: int) -> None:
        i = self.pos[x]
        self.total -= 1
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] -= 1
            i += i & -i

    def size(self) -> int:
        return self.total

    def get(self, k: int) -> int:
        idx = 0
        step = self.step
        bit = self.bit
        n = self.n
        while step:
            nxt = idx + step
            if nxt <= n and bit[nxt] < k:
                idx = nxt
                k -= bit[nxt]
            step >>= 1
        return self.vals[idx]

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        if not nums:
            return []

        tree = FenwickTree(nums)
        ans = []

        for i, x in enumerate(nums):
            tree.insert(x)

            if tree.size() > k:
                tree.remove(nums[i - k])

            if tree.size() == k:
                if k % 2 == 1:
                    ans.append(float(tree.get(k // 2 + 1)))
                else:
                    ans.append((tree.get(k // 2) + tree.get(k // 2 + 1)) / 2)

        return ans