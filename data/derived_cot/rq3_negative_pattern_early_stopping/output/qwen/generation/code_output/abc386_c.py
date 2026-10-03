def main():
    import sys
    data = sys.stdin.read().splitlines()
    K = int(data[0].strip())
    S = data[1].strip()
    T = data[2].strip()
    
    if S == T:
        print("Yes")
        return
        
    n = len(S)
    m = len(T)
    
    # Case 1: One replacement
    if n == m:
        count = 0
        for i in range(n):
            if S[i] != T[i]:
                count += 1
                if count > 1:
                    break
        if count == 1:
            print("Yes")
            return
            
    # Case 2: One deletion (from S) or one insertion (to S) -> which is equivalent to considering S and T with one character difference in length 1.
    # We can consider the case where |n - m| == 1.
    if abs(n - m) == 1:
        if n > m:  # then we need to delete one character from S
            i = 0
            j = 0
            found = False
            while i < n and j < m:
                if S[i] != T[j]:
                    # Skip the extra character in S
                    i += 1
                    found = True
                    break
                i += 1
                j += 1
            if found and i == n and j == m:
                print("Yes")
                return
            # Alternatively, if we didn't break, then the strings are equal except for the length, but we must have exactly one deletion.
            # But note: we break at the first mismatch. However, we must ensure that after skipping one, the rest matches.
            # The above while loop breaks at the first mismatch and then skips one in S and then continues. But if there are multiple mismatches, we break and then check if we reached the end.
            # Actually, we can do: after skipping one, the rest must match.
            # But the above while loop does not cover the case where the mismatch happens at the end? Actually, we break at the first mismatch and then continue from the next index.

            # Alternatively, we can use two pointers and skip one deletion and check if the rest matches.

            # Let's re-implement the deletion check properly.

            # We'll use two pointers and skip one deletion and then check if the rest of the string matches.
            # Actually, the above while loop is incomplete because if the mismatch happens at the beginning, then we skip one and then the rest must match.

            # But note: the above while loop condition: we break at the first mismatch and then skip one and then continue. However, if the mismatch is at the beginning, then we break and then the rest of the string must match from the next index.

            # Actually, the above while loop does not work correctly. Let me fix it.

            # We can do: traverse both strings with two pointers, and if we find a mismatch, then we skip one from S (the longer one) and then continue. If we reach the end of T, then it's valid.

            # Let me rewrite the deletion check:

            i = 0
            j = 0
            while i < n and j < m:
                if S[i] != T[j]:
                    # Skip one in S (the longer one) and break the current mismatch
                    i += 1
                    # Then continue the comparison from the next index
                    break
                i += 1
                j += 1
            # Now, if we broke because of a mismatch, then we must have skipped one and then the rest must match.
            if i == n and j == m:
                print("Yes")
                return