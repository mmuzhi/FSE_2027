def main():
    S = input().strip()
    n = len(S)
    # If the string is empty, return 0
    if n == 0:
        print(0)
        return

    # We'll use dynamic programming (DP) to solve the problem.
    # Let dp[i] be the minimum number of button presses to display the prefix S[0:i]
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # empty string

    # We'll consider transitions for each position i (from 0 to n)