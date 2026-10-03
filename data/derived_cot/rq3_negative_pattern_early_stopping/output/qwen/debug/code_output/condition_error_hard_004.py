import collections

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        indexes = collections.defaultdict(collections.deque)
        for index, character in enumerate(s):
            indexes[int(character)].append(index)
        
        unique_t_values = set(int(char) for char in t)
        for t_v in unique_t_values:
            if t_v not in indexes:
                return False
        
        for char in t:
            d = int(char)
            if d not in indexes:
                return False
            for x in range(d):
                if x in indexes and indexes[x] and indexes[x][0] < indexes[d][0]:
                    return False
            indexes[d].popleft()
            if not indexes[d]:
                del indexes[d]
        
        return True