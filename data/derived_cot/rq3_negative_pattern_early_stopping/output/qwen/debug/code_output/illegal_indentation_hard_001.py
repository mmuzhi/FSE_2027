class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        from collections import defaultdict, deque
        # Map each digit to a deque of its indices in s
        indexes = defaultdict(deque)
        for index, char in enumerate(s):
            digit = int(char)
            indexes[digit].append(index)
        
        # For each digit in t, we will try to find a matching digit in s
        # We need to ensure that for the current digit d in t, there is an occurrence in s that is not used and that is >= d, and also that we can remove it without violating the order.
        # But note: we are allowed to remove any digit from left to right, so we can remove the leftmost available digit that is >= d.
        # However, the condition in the original code was checking for the presence of smaller digits to the left, which was incorrect.

        # Let's change the approach: we will maintain the current available indices for each digit.
        # But note: the original code used a dictionary of deques for s.

        # We'll do:
        #   For each digit in t (in order):
        #       Let d = int(char)
        #       We need to find the smallest digit in s (that is >= d) that is available and then remove its leftmost occurrence.
        #       However, we cannot remove a digit that is not available.

        # But note: the original code did not check the condition on the removed digit being >= d. It only checked the positions of smaller digits.

        # We'll change the code to:

        #   For each digit d in t:
        #       If there is no occurrence of any digit >= d in s (that is available), return False.
        #       Then, remove the leftmost occurrence of the smallest digit >= d.

        # However, we need to know the smallest digit >= d that is available. We can do:

        #   We'll keep a list of available indices for each digit.

        #   But note: the original code used a deque for each digit. We can do:

        #       We'll create a list of deques for digits 0 to 9 (or just use the defaultdict) but we need to consider digits >= d.

        #   We can do:

        #       Let d_int = int(char)
        #       We'll look for the smallest digit >= d_int that has available indices.

        #   But note: we are allowed to remove any digit from left to right, so we should remove the leftmost available index of the smallest digit >= d_int.

        #   However, we must remove the leftmost available index of the smallest digit >= d_int to ensure we don't block a smaller digit for a future replacement.

        #   But wait, the replacement condition is that the removed digit must be >= d_int. So we can remove any digit >= d_int.

        #   We want to remove the leftmost available index of the smallest digit >= d_int because that is the earliest we can remove it.

        #   Steps:

        #       For each digit d in t:
        #           Let d_int = int(d)
        #           Let found = False
        #           For digit_val in range(d_int, 10):
        #               If digit_val is in indexes and the deque for digit_val is not empty and the leftmost index is the smallest available index for any digit >= d_int, then we remove that index and break.
        #           But note: we want the leftmost index overall for any digit >= d_int.

        #   We can do:

        #       We'll keep a list of the leftmost available indices for each digit, but we need to consider all digits >= d_int.

        #   Alternatively, we can precompute the leftmost available index for each digit and then take the minimum index among digits >= d_int.

        #   However, we are removing indices, so we need to update the available indices.

        #   We can do:

        #       We'll maintain a list (or array) of deques for digits 0-9.

        #       Then, for each digit d in t:
        #           Let d_int = int(d)
        #           Let candidate_index = None
        #           Let candidate_digit = None
        #           For digit_val in range(d_int, 10):
        #               If digit_val in indexes and indexes[digit_val] is not empty and (candidate_index is None or indexes[digit_val][0] < candidate_index):
        #                   candidate_index = indexes[digit_val][0]
        #                   candidate_digit = digit_val
        #           If candidate_index is None: return False
        #           Then, remove candidate_index from indexes[candidate_digit]

        #   But note: the original code did not do this. It only checked for the existence