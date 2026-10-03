# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:

        # first calculate the length
        length = 0
        ptr = head
        while ptr:
            length += 1
            ptr = ptr.next

        # Calculate base and remainder
        base = length // k
        remainder = length % k
        
        # Create an array for the number of nodes in each part
        part_lengths = []
        for i in range(remainder):
            part_lengths.append(base + 1)
        for i in range(remainder, k):
            part_lengths.append(base)
        
        # Now, split the list
        result = []
        current = head
        for part_length in part_lengths:
            # If part_length is 0, then we append None and move on.
            if part_length == 0:
                result.append(None)
                continue
            
            # For the current part, we need to move 'part_length' nodes, but the last node of the part should be the one at part_length-1.
            # So we move part_length - 1 steps to set the end of the part, then the next node is the start of the next part.
            part_head = current
            if part_length > 1:
                # Move part_length - 1 steps
                steps = part_length - 1
                while steps and current:
                    current = current.next
                    steps -= 1
                # Now, current is the last node of the current part, so set its next to None and append the part_head.
                if current:
                    current.next = None
            # If part_length is 1, then we just set current to None (but we don't need to move) and append the part_head.
            result.append(part_head)
            # Move current to the next part
            if current:
                current = current.next
        
        # If we have less than k parts, we pad with None
        while len(result) < k:
            result.append(None)
        
        return result