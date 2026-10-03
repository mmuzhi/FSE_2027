class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        arr = [0] * (n+1)
        for lv, ar, seats in bookings:
            arr[lv-1] += seats
            arr[ar] -= seats
        return list(accumulate(arr[:n]))  # We take the first n elements (indices 0 to n-1) and do prefix sum

# But wait, the original code used arr[:-1] which is the same as arr[:n] because arr has length n+1.
# However, let me check: arr[:n] is the first n elements (indices 0 to n-1). arr[:-1] is the same.

# But note: the booking might have ar equal to n, then we subtract at arr[n] (which is the last element). 
# Then when we do arr[:n] we are excluding the last element (index n) so that is correct.

# However, the original code used arr[:-1] which is the same as arr[:n] (since the array has length n+1, arr[:-1] is the first n elements).

# But wait, the original code had a bug because it used arr[ar+1] which might be out of bounds. Now we use arr[ar] which is safe because ar is at most n (so index ar is in [0, n] and we have an array of length n+1).

# However, note that the booking's `ar` is the end day, and the problem says the booking is for days from `lv` to `ar` (inclusive). 
# Our method: 
#   We add at lv-1 and subtract at ar (which is the next day after the last day we want to cover). 
#   Then the prefix sum at day i (which is the i-th day) is the sum of the difference array from index0 to index i-1.

# But note: the prefix sum at day i is the sum of arr[0] to arr[i-1]. 

# However, the standard difference array technique for [l, r] (inclusive) is:
#   diff[l-1] += value
#   diff[r]   -= value

# Then the prefix sum at index i (0-indexed) gives the value for day i+1.

# But in our code, we are returning the prefix sum of the first n elements (which are the differences for days 1 to n). 

# Actually, let me reindex:

#   We have an array `arr` of length n+1 (indices 0 to n).
#   We do:
#       arr[lv-1] += seats
#       arr[ar]   -= seats

#   Then the prefix sum at index i (0-indexed) is the total seats for day i+1.

#   But note: the problem expects an array of length n (for days 1 to n). 

#   The prefix sum of the first n elements (indices 0 to n-1) gives the seats for day1 to day n.

#   However, the standard difference array technique usually uses an array of length n (for days 1 to n) and then we do:

#       diff = [0]*(n+1)
#       for each booking [l, r, seats]:
#           diff[l-1] += seats
#           diff[r]   -= seats
#       Then the answer for day i is the prefix sum of diff from 0 to i-1.

#   But note: the prefix sum of the entire diff array (without excluding the last element) would give the value for day i as the prefix sum up to index i-1.

#   In our code, we are returning the prefix sum of the first n elements (which is the same as the prefix sum of the entire diff array without the last element). 

#   However, the last element (index n) is not used in the prefix sum because we are only taking the first n elements.

#   This is correct because the booking that ends at day n (ar = n) subtracts at index n (the last element) and that subtraction is not included in the prefix sum for day n (which is the prefix sum of the first n elements, i.e., indices 0 to n-1).

#   Therefore, the code is fixed.

# But wait, the original code used `arr[ar+1]` which is incorrect. We changed it to `arr[ar]`.

# Let me test with the example [1,3,10] and n=3:

#   arr = [0,0,0,0]
#   After booking: arr[0] = 10, arr[3] = -10
#   Then arr[:3] = [10,0,0] (if we take the first 3 elements, but note: arr has 4 elements, so arr[:3] is [10,0,0])
#   Then accumulate([10,0,0]) -> [10,10,10] which is correct.

# However, note that the original code used `arr[:-1]` which is the same as `arr[:n]` because the array has length n+1.

# So we can write:

#   return list(accumulate(arr[:n]))

# But note: the array `arr` has length n+1, so `arr[:n]` is the first n elements.

# Alternatively, we can use `arr[:-1]` because `arr[:-1]` is the same as `arr[:n]` (since the array has length n+1, the last element is at index n, and `arr[:-1]` goes from 0 to n-1).

# However, to be explicit and avoid any confusion, we can use `arr[:n]`.

# But note: the problem says the bookings are for days from `lv` to `ar` (inclusive). We are using the standard difference array technique.

# Final code:

class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        arr = [0] * (n+1)
        for lv, ar, seats in bookings:
            arr[lv-1] += seats
            arr[ar] -= seats
        return list(accumulate(arr[:n]))