def main():
    S = input().strip()
    T = input().strip()
    
    n = min(len(S), len(T))
    for i in range(n):
        if S[i] != T[i]:
            print(i+1)
            return
            
    # If we exit the loop, then the first n characters are the same.
    if len(S) == len(T):
        print(0)
    else:
        # The first difference is at the position after the common part.
        # The common part is of length n, so the next position is n+1.
        # But note: the condition says the smallest i that is in the range of the longer string and beyond the shorter.
        # Since the common part is n, then the first differing position is n+1.
        print(n+1)

if __name__ == "__main__":
    main()