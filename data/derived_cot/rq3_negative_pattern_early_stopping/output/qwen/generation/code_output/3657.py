class Solution:
    def checkValidCuts(self, n: int, rectangles: List[List[int]]) -> bool:
        # Separate the rectangles for horizontal and vertical cases.
        # For horizontal cuts, we need to find two y-coordinates a and b (0 <= a < b <= n) such that:
        #   All rectangles with end_y <= a are in the bottom.
        #   All rectangles with start_y >= b are in the top.
        #   The rest (with start_y < b and end_y > a) must have start_y >= a and end_y <= b (to be in the middle).
        # Similarly for vertical cuts.

        # First, try horizontal cuts.
        # We can consider candidate y-coordinates from the set of all start_y and end_y.

        # But note: the constraints: n up to 10^9, rectangles up to 10^5.

        # We can try to find candidate cuts from the unique y-coordinates that are either start_y or end_y.

        # However, we can use a different approach.

        # For horizontal cuts, we can consider the following:
        #   Let A be the set of rectangles that are entirely in the top (start_y >= b) and the set of rectangles that are entirely in the bottom (end_y <= a). Then the rest must be in the middle.

        # But we need to choose a and b (with a < b) such that:
        #   a is at least the maximum end_y of the bottom rectangles (if any) and less than the minimum start_y of the top rectangles (if any) and the middle rectangles must fit in [a, b].

        # Alternatively, we can think greedily:

        # For horizontal cuts:
        #   We need to choose a and b (0 <= a < b <= n) such that:
        #       1. All rectangles with end_y <= a are in the bottom.
        #       2. All rectangles with start_y >= b are in the top.
        #       3. For the remaining rectangles, we must have a <= start_y and end_y <= b.

        # We can try to find a candidate a as the maximum end_y of the bottom rectangles (if we have any bottom rectangles) and then candidate b as the minimum start_y of the top rectangles (if we have any top rectangles). Then, check if the remaining rectangles (neither bottom nor top) have start_y >= a and end_y <= b.

        # But note: we don't know which rectangles are bottom and top. We can try to find a candidate a and b by scanning the y-coordinates.

        # However, we can use the following:

        #   Let's collect all unique y-coordinates from the rectangles (both start_y and end_y) and sort them. Then, consider candidate cuts at these coordinates.

        # But note: the problem constraints (10^5 rectangles) so we can collect up to 200,000 unique y-coordinates.

        # Steps for horizontal:

        #   Let ys = sorted(set(all start_y and end_y))

        #   We need to choose two indices i and j (i < j) such that:
        #       a = ys[i], b = ys[j]

        #   Then, check:
        #       For each rectangle:
        #           if end_y <= a: bottom
        #           elif start_y >= b: top
        #           else: must have start_y >= a and end_y <= b (middle)

        #   But we must ensure that the bottom rectangles are exactly those with end_y <= a, and top with start_y >= b, and the rest are middle.

        # But note: a rectangle might be both bottom and top? No, because if a rectangle has end_y <= a and start_y >= b, then a >= end_y and b <= start_y, so a >= end_y >= start_y >= b, which implies a >= b, which is not allowed (a < b). So, no rectangle can be both.

        # However, we must also ensure that the bottom and top sections are non-empty? Actually, the problem says "each of the three resulting sections contains at least one rectangle". So, we need at least one rectangle in bottom, one in middle, and one in top.

        # But wait, the problem says "each of the three resulting sections formed by the cuts contains at least one rectangle". So, we need three sections, each with at least one rectangle.

        # So, we must have at least one rectangle in bottom, one in middle, and one in top.

        # Now, how to choose a and b? We can try to find a candidate a from the set of end_y (for bottom rectangles) and candidate b from the set of start_y (for top rectangles) such that a < b.

        # Alternatively,