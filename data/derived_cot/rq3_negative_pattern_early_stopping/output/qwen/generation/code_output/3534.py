class Solution:
    def countPairs(self, nums: List[int]) -> int:
        from collections import defaultdict
        def get_swaps(n):
            s = str(n)
            n = len(s)
            swaps = set()
            for i in range(n):
                for j in range(i+1, n):
                    # Swap digits at i and j
                    arr = list(s)
                    arr[i], arr[j] = arr[j], arr[i]
                    # Convert back to string and remove leading zeros if any
                    swapped_str = ''.join(arr)
                    # If the swapped string has leading zeros, we can convert to int to remove them, but note: the problem allows leading zeros, but the numbers are positive integers. However, the operation is on the string representation. But note: the problem says "swap any two digits", so we should consider the string representation with possible leading zeros.
                    # But the problem says: "it is allowed for an integer to have leading zeros after performing an operation." So, we should consider the swapped string as is, but then compare with the other number's string representation (which might have leading zeros too).
                    # However, the original numbers are positive integers, so they don't have leading zeros. But after swapping, they might. So, we should compare the swapped string (with possible leading zeros) to the other number's string representation (without leading zeros) or with leading zeros? Actually, the problem says "can become equal", meaning the integer value? Or the string representation?

                    # Let me check the example: 3 and 30. 30 swapped to 03, which is 3. So, the integer value is the same. But if we have 10 and 1, then 10 swapped to 01 (which is 1). So, the integer value is the same.

                    # Therefore, we can convert both the original number and the swapped number to integers and then compare? But wait, the problem says "swap any two digits", so the operation is on the digits. But then, the resulting number is the integer formed by the digits, which might have leading zeros. But in integer terms, leading zeros don't count. So, 03 is 3.

                    # However, the problem says "after performing the operation", so the operation is done on the digit string. But then, the resulting number is the integer value of that string. So, we can convert the swapped string to an integer and then compare with the other number (converted to integer) or with the string representation?

                    # Actually, the problem says: "two integers x and y are almost equal if both integers can become equal after performing the operation at most once." So, the operation is performed on one of the integers. The operation is defined as swapping two digits in the chosen number. Then, the two integers (the original x and y) are almost equal if after at most one swap (on one of them) they become equal.

                    # So, we can consider two numbers x and y. We can either swap in x to get y, or swap in y to get x. But note, the operation is at most once, and we can choose which number to swap.

                    # Therefore, for two numbers x and y, they are almost equal if:
                    #   Either x can be transformed into y by one swap (on x), or y can be transformed into x by one swap (on y).

                    # But note: swapping is symmetric? Not exactly. For example, 12 and 21: swapping 12 gives 21, but swapping 21 gives 12. So, both ways work. But also, 100 and 10: swapping 100 (swap the last two zeros) gives 100 -> 100 (same) but wait, that doesn't help. Alternatively, swapping 100 to get 010 (which is 10) is one swap. So, 100 can be transformed into 10 by one swap. But 10 cannot be transformed into 100 by one swap because 10 has two digits and 100 has three. So, the operation is on the digit string, and the digit string of 10 is "10", and swapping the two digits gives "01", which is 1. So, 10 cannot become 100 by swapping because the digit lengths must match? Actually, no: the operation is defined on the digits of the number. The number 10 has two digits, so swapping two digits in 10 gives a two-digit number. But 100 has three digits. So, to swap in 10 to get a three-digit number, you can't because 10 only has two digits. Therefore, the operation is only allowed on the digits