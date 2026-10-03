class Solution:
    def minimumPartition(self, s: str, k: int) -> int:
        n = len(s)
        # If k is 0, then we cannot have any digit that is not '0'
        # But note: the problem says "partition the string", so we must break the string into parts that are numbers <= k.
        # We'll traverse the string and form numbers.
        ans = 0
        curr = 0
        for i in range(n):
            # Append the current digit
            curr = curr * 10 + int(s[i])
            # If the current number exceeds k, then we break the partition at the previous digit
            if curr > k:
                # But note: we cannot break in the middle of a digit? Actually, we break the string at the previous digit and start a new number with the current digit.
                # However, we must reset the current number to the current digit and increment the partition count.
                # But first, we need to reset the current number to the current digit and then check if that digit alone is <= k.
                # However, note: the current digit might be greater than k? Then we cannot form a number with it.
                # But the problem says: if any digit is greater than k, then we return -1.
                # Actually, the condition in the original code checked each digit individually. But note: if we have a digit that is greater than k, then even as a single digit it is invalid.
                # So we must check: if the current digit (as a single digit) is greater than k, then we return -1.
                # But wait, the original code did that. However, in our corrected version, we are building the number. So if we have a digit that is greater than k, then when we try to form a single-digit number, it will be greater than k and then we reset? But resetting would set it to the same digit, which is still greater than k. Then we would have an invalid partition.

                # Actually, the problem requires that every substring is a number <= k. So if we have a digit that is greater than k, then we cannot use it as a single-digit number. Therefore, we must return -1.

                # But note: the original code checked each digit individually and returned -1 if any digit was greater than k. However, that is not entirely correct because the digit might be part of a multi-digit number that is <= k? Actually, no: if a digit is greater than k, then even as a single-digit number it is invalid. So the original code's check is correct.

                # However, in our corrected code, we are building the number. We must check at the beginning of the loop if the current digit is greater than k? Actually, we can check at the time of reset: if the current digit (which is the one that caused the overflow) is greater than k, then we cannot form a valid partition.

                # But note: the reset happens when the current number (which includes the current digit) exceeds k. Then we reset the current number to the current digit. But if the current digit is greater than k, then we cannot form a valid partition.

                # So we must check: if the current digit (as a single-digit number) is greater than k, then we return -1.

                # However, the original code did not do that. It only checked each digit individually. But note: the original code did:

                #   for d in s:
                #       if int(d) > k:
                #           return -1

                # So we must do that too.

                # But wait, in our corrected code, we are building the number. We haven't checked each digit individually. So we must check at the beginning of the loop or when we reset.

                # Actually, we can check at the beginning of the loop: if the current digit is greater than k, then we return -1.

                # However, note: the current digit might be part of a multi-digit number that is <= k? No, because if the current digit is greater than k, then even as a single-digit number it is invalid.

                # So let's change the approach:

                # We'll check each digit as we go. If the current digit is greater than k, then we return -1.

                # But wait, what if the current digit is part of a multi-digit number that is <= k? Actually, no: if the current digit is greater than k, then even if we break the string at the previous digit, the current digit alone is invalid.

                # Therefore, we must check: if the current digit (as a single-digit number) is greater than k, then we return -1.

                # However, note: the problem does not say that the numbers must be positive. But k is an integer and the digits are from '