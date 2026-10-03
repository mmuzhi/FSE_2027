import math

def main():
    R = int(input().strip())
    R_sq = R * R
    count = 0
    # We are going to iterate over i and j in a range. But note R can be up to 10^6, so we cannot iterate over all integers from -R to R (which would be 2*R+1 in each dimension, so about 4*R^2 points, which is 4e12 for R=10^6, too many).

    # Instead, we can use the condition: (i+0.5)^2 + (j+0.5)^2 <= R_sq, but note the condition is actually the maximum of the four corners, which is (|i|+0.5)^2 + (|j|+0.5)^2 <= R_sq? 

    # Actually, from the above examples, the condition for the entire square is that the maximum distance (which is the distance to the corner that is in the direction of the positive i and positive j, but considering absolute values) is <= R.

    # But note: the condition for the entire square is that the circle must contain the four corners. The four corners are (i±0.5, j±0.5). The condition is that the circle must contain the point (i+0.5, j+0.5) and the point (i+0.5, j-0.5) and (i-0.5, j+0.5) and (i-0.5, j-0.5). 

    # However, note that the condition for the entire square is equivalent to:
    #   (i+0.5)^2 + (j+0.5)^2 <= R_sq   AND   (i+0.5)^2 + (j-0.5)^2 <= R_sq   AND   (i-0.5)^2 + (j+0.5)^2 <= R_sq   AND   (i-0.5)^2 + (j-0.5)^2 <= R_sq

    # But wait, is that correct? Actually, no. The entire square is contained if and only if the circle contains all four corners. So we must check all four.

    # However, note that the four conditions are independent. But we can also note that the condition for the entire square is equivalent to:
    #   (i+0.5)^2 + (j+0.5)^2 <= R_sq   OR   (i+0.5)^2 + (j-0.5)^2 <= R_sq   OR   (i-0.5)^2 + (j+0.5)^2 <= R_sq   OR   (i-0.5)^2 + (j-0.5)^2 <= R_sq   is not the condition.

    # Actually, the condition is that the circle must contain the entire square. The entire square is contained if and only if the circle contains all four corners. So we must check all four.

    # But note: the four corners are the four points. The condition is that the circle must contain the point (i+0.5, j+0.5) and the point (i+0.5, j-0.5) and the point (i-0.5, j+0.5) and the point (i-0.5, j-0.5). 

    # However, we can also think: the square is contained in the circle if and only if the circle contains the entire square. The square is the set of points (x,y) such that i-0.5 <= x <= i+0.5 and j-0.5 <= y <= j+0.5. The condition is that the maximum distance from the origin to any point in the square is <= R. The maximum distance is the distance to the corner (i+0.5, j+0.5) if i and j are positive? Actually, the maximum distance is the distance to the corner that is farthest from the origin. The farthest corner is the one with the largest absolute value in both coordinates. So the condition is that the circle must contain the point (i+0.5, j+0.5) if i and j are positive? But if i is negative, then the farthest corner is (i-0.5, j+0.5) or (i-0.5, j-0.5). 

    # Actually, the condition is that the circle must contain the point (i+0.5, j+0.5) and the point (i+0.5, j-0.5) and the point (i-0.5, j+0.5) and the point (i-0.5, j