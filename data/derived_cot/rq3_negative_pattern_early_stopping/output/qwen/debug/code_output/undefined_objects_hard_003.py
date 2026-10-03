class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False
        ind = defaultdict(deque)
        for idx, char in enumerate(t):
            ind[char].append(idx)
        a = []
        for char in s:
            a.append(ind[char].popleft())
        n = len(a)
        bt = BIT(n)
        last_occurrence = [-1] * 10  # For digits 0-9

        for i in range(n):
            d = int(s[i])
            inv = bt.sum(n) - bt.sum(a[i])
            bt.update(a[i], 1)
            for dig in range(d-1, -1, -1):
                if last_occurrence[dig] >= i - inv:
                    return False
            last_occurrence[d] = a[i]
        return True
