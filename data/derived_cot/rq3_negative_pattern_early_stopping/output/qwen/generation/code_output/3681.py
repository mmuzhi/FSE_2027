class Solution:
    def maxRectangleArea(self, points: List[List[int]]) -> int:
        if len(points) < 4:
            return -1
        
        xs = sorted(set(x for x, y in points))
        ys = sorted(set(y for x, y in points))
        
        max_area = -1
        
        for i in range(len(xs)):
            for j in range(i+1, len(xs)):
                for k in range(len(ys)):
                    for l in range(k+1, len(ys)):
                        x1, x2 = xs[i], xs[j]
                        y1, y2 = ys[k], ys[l]
                        # Check if the four corners are present
                        corners = {(x1, y1), (x1, y2), (x2, y1), (x2, y2)}
                        if not corners.issubset(set(map(tuple, points))):
                            continue
                        # Check for any other point inside or on the border
                        valid = True
                        for px, py in points:
                            if (px == x1 or px == x2 or py == y1 or py == y2) and not ((px == x1 or px == x2) and (py == y1 or py == y2)):
                                # This point is on the border but not a corner
                                continue
                            elif x1 < px < x2 and y1 < py < y2:
                                # This point is strictly inside
                                valid = False
                                break
                        if valid:
                            area = (x2 - x1) * (y2 - y1)
                            if area > max_area:
                                max_area = area
        
        return max_area if max_area != -1 else -1