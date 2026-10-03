class Solution:
    def minArraySum(self, nums: List[int], k: int, op1: int, op2: int) -> int:
        n = len(nums)
        # We'll create two lists: one for Operation 1 and one for Operation 2.
        # But note: each index can use both operations at most once, so we need to consider combinations.
        # However, the operations are independent and can be applied in any order, but each at most once per index.
        # We can consider for each index the possible values after applying 0, 1 (for op1), and 1 (for op2) operations.
        # But note: Operation 2 requires the number to be >= k, and Operation 1 can be applied even if Operation 2 isn't.
        # We have a limited number of operations (op1 and op2) for the entire array, so we need to choose which indices to apply which operations optimally.

        # However, note the constraints: nums.length <= 100, and nums[i] <= 10^5, op1 and op2 <= nums.length (so at most 100 each). 
        # We can try a greedy approach: for each index, we can choose to apply Operation 1, Operation 2, both, or none, but the total number of Operation 1s used cannot exceed op1 and Operation 2s cannot exceed op2.

        # But 100 elements and two operations, each with up to 100 uses, but each index can use each operation at most once. So actually, for each index, we can use Operation 1 at most once and Operation 2 at most once, but the total uses across indices for Operation 1 cannot exceed op1 and for Operation 2 cannot exceed op2.

        # Actually, the problem says: "You can perform this operation at most op1 times, and not more than once per index." So for Operation 1, we can use it on at most op1 indices (each index at most once). Similarly for Operation 2.

        # So we have a fixed budget: we can apply Operation 1 to at most op1 indices, and Operation 2 to at most op2 indices.

        # The goal is to minimize the total sum.

        # We can think of it as: for each index, we have three choices:
        # 1. Do nothing: value = nums[i]
        # 2. Apply Operation 1: value = ceil(nums[i] / 2)
        # 3. Apply Operation 2: if nums[i] >= k, then value = nums[i] - k
        # 4. Apply both: value = ceil((nums[i] - k) / 2) if nums[i] >= k? But wait, the operations can be applied in any order. Actually, Operation 1 is division by 2 (rounding up) and Operation 2 is subtracting k. The order matters.

        # Let's consider the order:
        # If we apply Operation 1 first then Operation 2: 
        #   Start with x, then Operation 1: ceil(x/2), then Operation 2: if ceil(x/2) >= k, then subtract k -> ceil(x/2) - k
        # If we apply Operation 2 first then Operation 1:
        #   Start with x, then Operation 2: x - k, then Operation 1: ceil((x - k)/2)

        # We need to choose the order that gives the minimum value for each index, but also consider the budget constraints.

        # However, note that the operations are independent and can be applied at most once per index. So for each index, we can choose to apply:
        # - None
        # - Only Operation 1
        # - Only Operation 2 (if nums[i] >= k)
        # - Both, but then we have two possibilities: Operation 1 then Operation 2, or Operation 2 then Operation 1.

        # Actually, the problem does not specify the order, but the operations are defined independently. However, the order can affect the result. So for each index, we can consider four states (if both operations are applicable and the conditions hold).

        # But note: Operation 2 requires the number to be >= k. After Operation 1, the number might become less than k, so Operation 2 might not be applicable. Similarly, Operation 1 can be applied even if Operation 2 isn't.

        # So for each index, the possible values are:
        # 1. nums[i]
        # 2. ceil(nums[i] / 2)   [Operation 1]
        # 3. nums[i] - k          [Operation 2, if nums[i] >= k]
        # 4. ceil