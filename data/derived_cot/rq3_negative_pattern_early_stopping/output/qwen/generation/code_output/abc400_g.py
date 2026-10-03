import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        N = int(data[index]); K = int(data[index+1]); index += 2
        cakes = []
        for i in range(N):
            x = list(map(int, data[index:index+3]))
            index += 3
            cakes.append(x)
        
        # We are going to consider each cake as having three values: X, Y, Z.
        # The idea: we want to form pairs such that the maximum of the three sums is as high as possible.
        # Observation: the total price is the sum of the maximums of the three sums for each pair.
        # We can think of each cake having three scores. We want to form pairs that have high scores in at least one of the three.

        # Alternate approach: consider that the price of a pair is the maximum of the three sums. We can try to assign a value to each cake that is the maximum of its three attributes? But note: the three attributes are independent and the pair's price is the maximum of the three combined.

        # Another idea: consider that the total price is the sum of the maximums. We can try to maximize the total by ensuring that each pair has a high value in one of the three attributes.

        # But note: the same cake can only be used once.

        # Let's try to reframe: we have three separate lists of numbers (the X, Y, Z of each cake). We want to form pairs (each cake in one pair) and for each pair, we take the maximum of the three sums (X1+X2, Y1+Y2, Z1+Z2). We want to maximize the sum of these maximums.

        # We can consider that the total price is the sum over pairs of max(X_i+X_j, Y_i+Y_j, Z_i+Z_j).

        # How to solve? Maybe we can consider that the maximum total is achieved by having as many pairs as possible with high values in one of the three attributes.

        # Let's consider: if we sort the cakes by one attribute, say X, then the top K pairs in X would be the top 2K cakes (if we take the top two, then the next two, etc.). But the price of a pair is the maximum of the three sums, so if we take two high X cakes, then the X sum is high, but the Y and Z might be low. However, if we take two cakes that are high in one attribute, then the max might be that attribute's sum.

        # But note: we are allowed to choose any pairs. So, we can form pairs that are not necessarily adjacent in any attribute.

        # Another idea: consider that the total price is the sum of the maximums. We can try to assign each cake to a pair and then the price of the pair is the maximum of the three sums. We want to maximize the total.

        # We can use a greedy approach: consider that the maximum total is the sum of the top K maximums we can get from the three attributes. But note: a pair's price is the maximum of the three sums, so if we have a pair that has a high X sum, then that pair's price is at least the X sum, but if another attribute's sum is higher, then the price is that. So, we cannot simply take the top K X sums and then the top K Y sums and then the top K Z sums because a pair can only contribute one value (the maximum of the three).

        # However, note that the same cake can be used only once, so we cannot use the same cake in two different pairs.

        # Let's try to think of the problem as: we have three separate lists (X, Y, Z). We want to form K pairs (each pair is two indices) such that the sum of the maximums of (X_i+X_j, Y_i+Y_j, Z_i+Z_j) is maximized.

        # We can consider that the maximum total is the sum of the top K values from the three attributes, but each value must come from a pair and each cake can be used only once.

        # Actually, we can break down the total price into three parts: the price from X, the price from Y, and the price from Z. But note: the price of a pair is the maximum of the three, so if a pair has a high X sum, then the price is the X sum, and then the Y and Z sums of that pair don't matter for that pair's price. However, the same cake's other attributes might be used in other pairs.

        # This seems complicated.

        # Let