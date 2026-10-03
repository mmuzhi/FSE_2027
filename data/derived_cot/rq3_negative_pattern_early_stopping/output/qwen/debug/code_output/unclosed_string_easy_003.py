class Solution:
    def countPoints(self, rings: str) -> int:
        rod_colors = {}
        i = 0
        n = len(rings)
        while i < n:
            if i + 1 < n:
                color = rings[i]
                rod = rings[i + 1]
                if rod not in rod_colors:
                    rod_colors[rod] = set()
                rod_colors[rod].add(color)
            i += 2
        count = 0
        for colors in rod_colors.values():
            if len(colors) == 3:
                count += 1
        return count