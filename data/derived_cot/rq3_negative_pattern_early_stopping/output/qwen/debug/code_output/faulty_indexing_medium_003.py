class Solution:
    def checkValidString(self, s):
        st = []
        sr = []
        for i in range(len(s)):
            if s[i] == '(':
                st.append(i)
            elif s[i] == '*':
                sr.append(i)
            else:
                if st:
                    st.pop()
                elif sr:
                    sr.pop()
                else:
                    return False
        
        # Now, we have unmatched '(' in st and unmatched '*' in sr.
        # We need to match the unmatched '(' with the unmatched '*' by ensuring that the '*' is after the '('.
        # We'll use two pointers for the two lists (st and sr) which are in increasing order (by index).
        i = 0
        j = 0
        # We want to match the earliest unmatched '(' with the earliest unmatched '*' that is after it.
        # But note: we can use any unmatched '*' to close any unmatched '(' as long as the '*' is after the '('.
        # We can do: for each unmatched '(', find a unmatched '*' that is after it.
        # Since the lists are sorted, we can do:

        # We'll iterate over the unmatched '(' and unmatched '*' to see if we can match them.
        # We'll use two pointers: i for st and j for sr.
        # We want to match the smallest index of '(' with the smallest index of '*' that is greater than it.
        # But we can do:

        # Let's create two lists: st and sr (already in increasing order).
        # We'll try to match the '(' from left to right with the '*' from left to right, but only if the '*' is after the '('.

        # However, we can also match the '(' from right to left with the '*' from right to left.

        # Let's try matching from the rightmost unmatched '(' to the leftmost unmatched '*':

        # We'll sort the lists (they are already sorted).
        # Then, we'll use two pointers starting from the end.

        # But note: we want to match the earliest unmatched '*' that is after the '('.

        # Alternatively, we can do:

        #   Let i = 0  # pointer for st
        #   Let j = 0  # pointer for sr
        #   while i < len(st) and j < len(sr):
        #       if st[i] < sr[j]:
        #           i += 1
        #           j += 1
        #       else:
        #           j += 1

        #   Then, if i == len(st), then we matched all.

        # But this is the same as before.

        # Let's try with the example that failed earlier: st = [1,4], sr = [2,3]
        #   i=0, j=0: 1<2 -> i=1, j=1.
        #   i=1, j=1: 4<3 -> False, so j=2 -> j>=len(sr) -> break. i=1, so not matched.

        #   This is correct because the second '(' at 4 cannot be matched.

        #   Another example: st = [1,3], sr = [2,4]
        #       i=0, j=0: 1<2 -> i=1, j=1.
        #       i=1, j=1: 3<4 -> i=2, j=2 -> matched.

        #   Example: st = [1,2], sr = [3,4]
        #       i=0, j=0: 1<3 -> i=1, j=1.
        #       i=1, j=1: 2<4 -> i=2, j=2 -> matched.

        #   Example: st = [2,3], sr = [1,4]
        #       i=0, j=0: 2<1 -> False, so j=1.
        #       i=0, j=1: 2<4 -> i=1, j=2 -> matched.

        #   But wait, the unmatched '*' at index1 is before the first unmatched '(' at index2. We cannot use it to close the first '(' at index2 because the closing bracket must be after the opening. However, the algorithm above matches the first '(' with the '*' at index4 and the second '(' with nothing? Actually, in the example st = [2,3], sr = [1,4], the unmatched '*' at index1 is not used because we advanced j to 1 and then matched the first '(' with the '*' at index4. But the '*' at index1 is before the first '(' at index2, so it cannot be used to close the first '(' at index2. However, it can be used to close a '(' that is before index1?