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

        # Calculate the base number of nodes per part and the remainder
        base = length // k
        remainder = length % k

        # Create an array to store the number of nodes for each part
        arrange = []
        for i in range(k):
            if i < remainder:
                arrange.append(base + 1)
            else:
                arrange.append(base)

        # Now, we will traverse the linked list and split it into parts
        parts = []
        current = head
        index = 0
        for size in arrange:
            # If we are at the beginning of a new part, the part starts at the current node
            if current is not None:
                # We need to move 'size' nodes for this part
                # If the part has 0 nodes, we append None and move on
                if size == 0:
                    parts.append(None)
                    continue

                # If we are starting a new part, we need to move the current node to the next part's head after processing
                # But note: we are going to cut the list at the end of this part
                # We need to move 'size - 1' steps to find the end of the current part
                temp = current
                for _ in range(size - 1):
                    if temp:
                        temp = temp.next
                    else:
                        break

                # Now, temp is the last node of the current part (or None if we ran out of nodes)
                if temp:
                    # The next part starts at temp.next, so we set the current part's end to None
                    next_head = temp.next
                    temp.next = None
                    parts.append(current)
                    current = next_head
                else:
                    # If we ran out of nodes, then the rest of the parts should be None
                    parts.append(None)
                    # We break because the rest of the parts will be None
                    # But we still need to fill the remaining parts with None
                    # So we break and then later we will append None for the remaining parts
                    break
            else:
                # If current is None, then the rest of the parts are None
                parts.append(None)
                # We break because the rest of the parts will be None
                # But we still need to fill the remaining parts with None
                # So we break and then later we will append None for the remaining parts
                break

        # If we have less than k parts, we need to append None for the remaining parts
        while len(parts) < k:
            parts.append(None)

        return parts