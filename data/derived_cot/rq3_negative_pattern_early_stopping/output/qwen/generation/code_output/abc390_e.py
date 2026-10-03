import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
        
    n = int(data[0])
    X = int(data[1])
    foods = []
    index = 2
    for i in range(n):
        v = int(data[index]); a = int(data[index+1]); c = int(data[index+2])
        index += 3
        foods.append((v, a, c))
        
    # We are going to binary search on m (the minimum vitamin intake)
    # m can be from 0 up to (max possible for each vitamin, but note: we need at least m for all three)
    # The maximum m we can have is limited by the total available of each vitamin and the calorie constraint.
    # We can set high = min(max_v1, max_v2, max_v3) but we don't know the max for each. Alternatively, we can set high to a value that is definitely too high, say min(X, max_v1, max_v2, max_v3) but we don't know max_v1, etc. Alternatively, we can set high to 0 and then increase until we find the maximum m that satisfies the condition.

    # But note: the maximum m cannot exceed the maximum amount of each vitamin we can get with calorie <= X. However, we don't know the maximum for each vitamin independently because we have to satisfy all three.

    # Alternatively, we can set high to a value that is the maximum possible for one vitamin (but note: we need all three). The maximum m is at most the minimum of the maximums of each vitamin that we can get with calorie <= X. But we don't know that.

    # We can set high to 0 and then increase until we find the maximum m that satisfies the condition. But we can also set high to a value that is the maximum vitamin amount for one type that we can get with calorie <= X, but then we have to consider the other two.

    # Actually, we can set high to the maximum m such that m <= (some value). The maximum m cannot exceed the maximum vitamin amount for any type that we can get with calorie <= X. But note: we need at least m for each of the three. So m cannot exceed the minimum of the maximums for each vitamin.

    # However, we can set high to 0 and then do a binary search until we find the maximum m that satisfies the condition. But we must set a high bound.

    # Let's compute the maximum possible m for each vitamin independently (without considering the other vitamins) and then set high to the minimum of these maximums? But note: we are constrained by the same calorie budget. Actually, we are going to use the same set of foods for all three vitamins.

    # Alternatively, we can set high to 0 and then do a binary search from 0 to (max_vitamin) where max_vitamin is the maximum vitamin amount we can get from one type with calorie <= X. But note: we need to get at least m from each type, so m cannot exceed the maximum of the minimums we can get from each type? Actually, no.

    # Let's define:
    #   Let f1(m) = minimum calories needed to get at least m vitamin 1 (ignoring other vitamins)
    #   Similarly for f2(m) and f3(m). But note: we are allowed to use the same food for multiple vitamins? No, each food only gives one vitamin.

    # Actually, we can precompute for each vitamin type the minimal calories to get at least m of that vitamin. But then we have to combine the three.

    # However, note: we are allowed to use the same food only once. So the sets for each vitamin are independent? Actually, no: the same food cannot be used for two vitamins. So we have to choose a set of foods that covers all three vitamins.

    # We can use a DP that considers the three vitamins and the calorie constraint. But the state space would be (calories, v1, v2, v3) which is too big.

    # Another idea: we can use a two-dimensional DP for two of the vitamins and then check the third. But we have three.

    # Alternatively, we can use a state that is (v1, v2, v3) and then use DP with state (i, v1, v2, v3) but that state space is too big.

    # We need a better approach.

    # Insight: we are only concerned with the minimum of the three. We want to maximize m such that we have at least m in each.

    # We can use a DP that tracks the maximum of the minimum of the three vitamins? Actually, no.

    # Another idea: we can use a DP that tracks the three vitamins separately