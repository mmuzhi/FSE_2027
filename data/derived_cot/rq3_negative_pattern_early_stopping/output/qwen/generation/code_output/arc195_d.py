import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        n = int(data[index]); index += 1
        arr = list(map(int, data[index:index+n]))
        index += n
        
        # We are allowed to rearrange arbitrarily, so the problem reduces to:
        # We need to form as many contiguous blocks of the same number as possible at the beginning, but note that the deletion operation deletes a contiguous block of the same number at the beginning. However, we can also delete multiple blocks if they are adjacent and of the same number? Actually, no: the deletion operation deletes a contiguous block of the same number at the beginning. So, if we have [1,1,2,2], we can delete the first two 1's and then the next two 2's. But if we have [1,2,2], we can delete the two 2's only if they are at the beginning. So, we need to bring same numbers together at the beginning.

        # Actually, the problem is similar to the "minimum adjacent swaps to group all same elements" but then we have to account for the deletions. However, note that the deletion operation deletes a contiguous block of the same number at the beginning. So, we can think of it as: we want to form a sequence of runs (each run is a contiguous block of the same number) and then we can delete each run in one operation. But the catch is that we can only delete from the beginning. So, the order of the runs must be such that we can delete them one by one.

        # But note: we can rearrange arbitrarily (because adjacent swaps allow any permutation). So, the problem is: we can rearrange the array arbitrarily, and then we delete from left to right, each deletion being a contiguous block of the same number. But wait, the deletion operation deletes a contiguous block of the same number at the beginning. So, if we rearrange the array, we can form a sequence of runs. The total number of deletions is the number of runs. But the cost is the number of adjacent swaps to form the runs plus the number of deletions (which is the number of runs). However, we are allowed to interleave the operations: we can delete a run and then swap the remaining elements.

        # Actually, the problem is more complex because we can delete a run and then the sequence changes. But note: the deletion operation deletes a contiguous block from the beginning, so the rest of the sequence shifts left. Then, we can continue swapping and deleting.

        # Alternatively, we can think greedily: we want to delete as many elements as possible in each deletion operation. So, we want to form the longest possible run at the beginning. Then, we delete that run, and then form the next longest run from the remaining elements, and so on.

        # But note: the total number of operations is the number of deletions (each deletion deletes a run) plus the number of adjacent swaps needed to bring the elements of the next run to the front.

        # However, we can also consider that the entire sequence can be rearranged arbitrarily. So, the minimal number of operations is the minimal number of adjacent swaps to form a sequence of runs (each run being a contiguous block of the same number) and then the number of deletions is the number of runs. But wait, the problem allows deletion operations and swaps in any order. So, we can interleave them.

        # Actually, the problem is equivalent to: we can remove a contiguous block of identical elements from the beginning at any time, and we can swap adjacent elements arbitrarily. We want to minimize the total operations (swaps + deletions).

        # This is similar to the problem of "minimum adjacent swaps to group all same elements together" but with the added ability to delete from the front. However, note that deletion from the front doesn't require swaps if the block is already at the front.

        # Let me reframe: We can simulate the process by keeping track of the current sequence. But the constraints are that the total N over test cases is 200,000, so we need an efficient solution.

        # Observation: The deletion operation deletes a contiguous block of the same number at the beginning. So, the entire sequence must be partitioned into contiguous blocks (runs) of the same number. The order of the runs can be arbitrary because we can swap arbitrarily. Therefore, we can rearrange the entire sequence into a sequence of runs (each run being a contiguous block of the same number) and then delete each run in one operation. But note: the deletion operation deletes the entire run at the beginning. So, we can delete the runs in any order? Actually, no: because after deleting a run, the next run must be at the beginning.