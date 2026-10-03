import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
    n = int(data[0])
    D = int(data[1])
    points = []
    xs = []
    ys = []
    index = 2
    for i in range(n):
        x = int(data[index]); y = int(data[index+1]); index += 2
        xs.append(x)
        ys.append(y)
    
    xs.sort()
    ys.sort()
    
    # Precompute prefix sums for xs and ys
    prefix_x = [0] * n
    prefix_x[0] = xs[0]
    for i in range(1, n):
        prefix_x[i] = prefix_x[i-1] + xs[i]
    
    prefix_y = [0] * n
    prefix_y[0] = ys[0]
    for i in range(1, n):
        prefix_y[i] = prefix_y[i-1] + ys[i]
    
    def f(x):
        # Find the position where x would be inserted in xs
        pos = bisect_left(xs, x)
        # Number of elements <= x
        left_count = pos
        # Number of elements > x
        right_count = n - pos
        # Sum of elements <= x
        if left_count > 0:
            left_sum = prefix_x[pos-1] + x * left_count - (prefix_x[pos-1] if pos-1 >= 0 else 0)
            # Actually, we have the prefix sum for xs[0:pos]
            # The sum of xs[0:pos] is prefix_x[pos-1] (if pos>0) else 0.
            # Then, the sum of absolute differences for the left part is (x * left_count - (sum of xs[0:pos]))
            left_sum_val = x * left_count - (prefix_x[pos-1] if pos > 0 else 0)
        else:
            left_sum_val = 0
        # Sum of elements > x
        if right_count > 0:
            # The sum of xs[pos:] is prefix_x[-1] - (prefix_x[pos-1] if pos>0 else 0) + xs[pos] if pos==0 then subtract nothing?
            # Actually, the sum of xs[pos:] is prefix_x[-1] - (prefix_x[pos-1] if pos>0 else 0)
            right_sum_val = (prefix_x[-1] - (prefix_x[pos-1] if pos>0 else 0)) - x * right_count
        else:
            right_sum_val = 0
        return left_sum_val + right_sum_val

    # But the above f(x) is not correct because the prefix_x array is built from the sorted xs, but the prefix_x[i] is the sum of the first i+1 elements.

    # Let me correct the f(x) function:

    # Actually, we can compute the sum of absolute differences by:
    # Let pos = bisect_left(xs, x)
    # Then, the left part: xs[0:pos] are <= x, and xs[pos:] are > x.
    # Then, the sum for the left part is (x * pos - (sum of xs[0:pos]))
    # The sum for the right part is ((sum of xs[pos:]) - x * (n - pos))

    # We have prefix_x for the entire array, so we can get the sum of xs[0:pos] as prefix_x[pos-1] if pos>0, else 0.
    # But our prefix_x is built as the cumulative sum of xs, so prefix_x[i] = xs[0]+...+xs[i].

    # So, for left part: if pos==0, then left_sum = 0, else left_sum = x * pos - prefix_x[pos-1]
    # For right part: if pos==n, then right_sum = 0, else right_sum = (prefix_x[n-1] - (prefix_x[pos-1] if pos>0 else 0)) - x * (n - pos)  -> but wait, the sum of xs[pos:] is prefix_x[n-1] - (prefix_x[pos-1] if pos>0 else 0) is not correct because prefix_x is built for the entire array.

    # Actually, we should precompute the entire prefix sum for xs and then use:
    # left_sum = x * pos - (prefix_x[pos-1] if pos>0 else 0)
    # right_sum = (prefix_x[n-1] - (prefix_x[pos-1] if pos>0 else 0)) - x * (n - pos)