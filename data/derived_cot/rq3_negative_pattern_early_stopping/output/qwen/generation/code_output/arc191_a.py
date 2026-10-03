import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    n, m = map(int, data[0].split())
    S = data[1].strip()
    T = data[2].strip()
    
    # We'll use a list for the final digits of length n.
    # We'll also keep track of the available operations (their digits and indices) but we only care about the digits and the order.
    # But note: we must use all operations, so we have to assign each operation to a position.
    # The final digit for a position is the digit from the last operation assigned to it.
    # We can assign the operations arbitrarily.

    # We want to maximize the integer.

    # We'll use a greedy algorithm that, for each position (from left to right), will choose the largest available digit from the remaining operations, but we must ensure that we can assign the remaining operations to the remaining positions.

    # However, note: the final digit for a position is the last operation assigned to it. So we can choose to not fix the digit for a position until the last operation assigned to it.

    # But we must use all operations.

    # We can use a two-pointer approach:

    # Let's consider that we will assign the operations in increasing order of k. But we can assign them arbitrarily to positions.

    # We can use a stack or a pointer to the best available digit.

    # Alternatively, we can consider that the final digit for a position is the digit from the last operation assigned to it.

    # We can reserve the best digits for the left positions.

    # We'll try to assign the largest digits in T to the left positions, but we must ensure that we can assign the remaining digits to the remaining positions.

    # But note: we can assign the same position multiple times, so the final digit for a position is the last assigned digit.

    # We can use a greedy algorithm that, for each position (from left to right), will choose the largest available digit from the remaining operations, and then remove that operation.

    # But then, for the remaining positions, we can choose the largest available digits.

    # However, the catch: if we choose a large digit from an early operation, then a later operation might have a larger digit, and if we assign that later operation to the same position, then the final digit for that position will be the larger one.

    # But then, why not choose the largest available digit for the current position? 

    # Because the largest available digit might be from a late operation, and if we choose it now, then we cannot use it for a later position.

    # But note: we are forming an integer from left to right. The leftmost digits have more significance.

    # However, consider: if we choose a large digit from a late operation for the leftmost position, then we are using a large digit for the leftmost position, which is good.

    # But then, how do we ensure that we can assign the remaining operations to the remaining positions?

    # We can assign the remaining operations arbitrarily to the remaining positions.

    # The only constraint is that the final digit for a position is the last operation assigned to it.

    # We can use a greedy algorithm that, for each position (from left to right), does the following:

    #   Let's say we have a list of available operations (each with a digit and an index k). We want to choose the largest digit available.

    #   But then, we must ensure that we can assign the remaining operations to the remaining positions.

    #   However, the catch: if we choose an operation with index k for the current position, then we cannot use any operation with index > k for the current position.

    #   But we can use operations with index > k for other positions.

    #   So the only constraint is that we must be able to assign the remaining operations to the remaining positions.

    #   But note: we can assign the remaining operations arbitrarily, so the only constraint is that the number of remaining operations is equal to the number of remaining positions plus the number of times we overwrite the current position (but we can overwrite any position arbitrarily).

    #   Actually, we must assign each operation to a position. There is no constraint on the number of times a position is overwritten.

    #   Therefore, the only constraint is that we have to use all operations.

    #   So we can choose any operation for the current position.

    #   But then, why not choose the largest available digit for the current position?

    #   Because the largest available digit might be from a late operation, and if we choose it now, then we are using a large digit for the current position, which is good.

    #   However, if we choose a large digit from a late operation for the current position, then we are using that operation for