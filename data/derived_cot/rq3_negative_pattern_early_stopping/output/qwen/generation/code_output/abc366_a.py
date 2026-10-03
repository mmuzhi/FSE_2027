def main():
    import sys
    data = sys.stdin.read().split()
    N = int(data[0])
    T = int(data[1])
    A = int(data[2])
    majority = (N + 1) // 2
    if T >= majority or A >= majority:
        # But note: if T is exactly majority, then Takahashi wins. Similarly for Aoki.
        # However, we must check: if T is exactly majority, then even if all remaining votes go to Aoki, Takahashi still has majority (because the remaining votes are not enough to change the majority if T is already majority).
        # But wait, what if T is exactly majority? Then the remaining votes are N - T - A. The maximum Aoki can get is A + (N - T - A) = N - T.
        # Then Takahashi has T, and Aoki has N - T. Since T = majority, then N - T = N - (N+1)//2 = (N-1)//2, which is less than majority.
        # So yes, if T is at least majority, Takahashi wins. Similarly for Aoki.
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()