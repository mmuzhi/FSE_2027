def count_steps(curr):
    steps = 0
    first = curr
    last = curr
    while first <= n:
        steps += min(last, n) - first + 1
        first *= 10
        last = last * 10 + 9
    return steps