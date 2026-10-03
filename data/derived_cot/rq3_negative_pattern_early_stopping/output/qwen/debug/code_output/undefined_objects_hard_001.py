class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if not head:
            return head
        
        # Dummy node to simplify the reversal at the beginning
        dummy = ListNode(0, head)
        prev_group_end = dummy
        
        while True:
            # Find the kth node from prev_group_end
            curr = prev_group_end
            count = k
            while count and curr.next:
                curr = curr.next
                count -= 1
            # If we didn't find k nodes, break
            if count != 0:
                break
            
            # curr is the end of the current group
            # The start of the group is prev_group_end.next
            group_start = prev_group_end.next
            
            # Reverse the group from group_start to curr
            prev_node = None
            curr_node = group_start
            # We need to reverse k nodes
            for i in range(k):
                next_node = curr_node.next
                curr_node.next = prev_node
                prev_node = curr_node
                curr_node = next_node
            
            # After reversing, the group_start becomes the tail of the reversed segment
            # And the reversed segment starts at prev_node (which is curr_node before the reversal? Actually, after reversal, prev_node is the last node of the reversed segment)
            # Now, attach the reversed segment to the main list
            prev_group_end.next = prev_node
            
            # The next group should start from the node after the reversed segment
            # The reversed segment's tail is group_start, and its next is curr_node (which is the node after the reversed segment)
            group_start.next = curr_node
            
            # Move prev_group_end to the end of the reversed segment (which is group_start)
            prev_group_end = group_start
            
            # If we've reached the end, break
            if not prev_group_end.next:
                break
        
        return dummy.next