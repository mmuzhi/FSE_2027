import collections

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        indexes = collections.defaultdict(collections.deque)
        for i, ch in enumerate(s):
            indexes[int(ch)].append(i)

        for ch in t:
            d = int(ch)
            if d not in indexes or not indexes[d]:
                return False
            idx = indexes[d][0]
            for smaller in range(d):
                if smaller in indexes and indexes[smaller] and indexes[smaller][0] < idx:
                    return False
            indexes[d].popleft()
            if not indexes[d]:
                del indexes[d]

        return True