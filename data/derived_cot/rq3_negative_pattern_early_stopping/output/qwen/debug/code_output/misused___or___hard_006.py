from collections import defaultdict

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        N = len(points)
        if N <= 2:
            return N
        
        D = defaultdict(set)
        for i in range(N):
            x1, y1 = points[i]
            for j in range(i+1, N):
                x2, y2 = points[j]
                if y1 == y2:
                    # Horizontal line: slope is 0, and we can represent the line by (0, y1) but note: multiple horizontal lines with same y1 are the same line.
                    key = (0, y1)
                elif x1 == x2:
                    # Vertical line: slope is undefined, represented by 'inf' and the x-coordinate.
                    key = ('inf', x1)
                else:
                    # General line: slope and intercept
                    # We can represent the line by (slope, intercept) but we must avoid floating point inaccuracies.
                    # Instead, we can use a tuple of fractions or a normalized representation.
                    # Let's use: (dy, dx) for slope and then intercept can be derived from one point: y = (dy/dx)*x + (y1*dx - x1*dy)/dx
                    # But note: we want to avoid floating point. We can represent the line by (dy, dx, c) but then we have to normalize the representation.
                    # Alternatively, we can use the two-point form: (x1*(y2-y1) - x2*(y1-y2)) = 0, but that's not a unique representation.
                    # Instead, we can use the normalized form: (dy, dx, c) but then we have to normalize the signs and the gcd.
                    # However, note that the problem does not require the line to be uniquely represented by integers, but we must avoid floating point inaccuracies.
                    # Let's use a tuple (dy, dx, c) but then we have to compute c. But note: we can also use the two-point form without intercept by using the equation: (y2-y1)*(x-x1) = (x2-x1)*(y-y1). But that doesn't help for grouping.
                    # Alternatively, we can use the normalized vector (dx, dy) and then the intercept in a normalized way? But note: two lines with the same slope but different intercepts are different.

                    # Actually, we can represent the line by the normalized direction vector and then the intercept. But to avoid floating point, we can use the following:
                    # Let dx = x2 - x1, dy = y2 - y1.
                    # Then the line can be represented by (dy, dx, -dx*y1+dy*x1) but then we have to normalize the entire tuple.

                    # However, note: the original code used two different formulas for the intercept. Let's fix the representation.

                    # We can represent the line by (dy, dx, c) where c = dy*x1 - dx*y1? Actually, the standard form is: dy*x - dx*y = dy*x1 - dx*y1.
                    # But then we can use the tuple (dy, dx, dy*x1 - dx*y1) but then we must normalize the signs and the gcd.

                    # But note: the problem is that the original code used two different formulas for the intercept. Let's change the representation to avoid floating point.

                    # We'll represent the line by a tuple (a, b, c) where the line equation is a*x + b*y + c = 0, but normalized.

                    # Alternatively, we can use the two-point form without intercept by storing the normalized direction and a point? But that's not unique.

                    # Let's stick to the normalized representation of the line equation in the form (dy, dx, c) but normalized by the gcd and sign.

                    dx = x2 - x1
                    dy = y2 - y1
                    # We want to normalize the direction vector (dx, dy) by the gcd and then the sign.
                    g = gcd(dx, dy)
                    if g != 0:
                        dx //= g
                        dy //= g
                    # Now, the line equation: dy*x - dx*y = dy*x1 - dx*y1
                    # But note: we can also represent by (dy, -dx, dy*x1 - dx*y1) but then we have to normalize the entire tuple.

                    # However, note: the original code used two different formulas for the intercept. We are going to change the representation to avoid floating point and to have a unique representation.

                    # But wait, the original code used two different formulas for the intercept. We are going to fix the representation by using integer arithmetic.

                    # Let's define the line by (dy, dx, c) where