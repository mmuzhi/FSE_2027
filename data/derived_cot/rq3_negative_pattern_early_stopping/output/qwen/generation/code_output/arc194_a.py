import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # We are going to use a stack to simulate the process, but we need to decide which elements to keep.
    # Alternatively, we can use a dynamic programming or a greedy method.

    # Observation: We can use a stack to keep track of the elements we are going to keep, and we can pop when the current element is less than the top (if we are trying to maximize the sum) but note: we can also keep negative numbers.

    # Actually, we can use a stack to simulate the process of building the sequence. We want to maximize the sum.

    # We can use a stack and push all positive numbers and pop negative numbers? But note: sometimes we might want to keep a negative number if it is the only one left? 

    # Alternatively, we can use a stack and maintain the maximum sum we can have at each step.

    # We can use a stack to keep the elements that we are going to keep. The idea is to pop from the stack when the current element is less than the top (if we are building a non-decreasing sequence) but that is for maximum rectangle.

    # Actually, we can use a similar idea as the "largest rectangle in a histogram" but here we are building a sequence and we can choose to pop arbitrarily.

    # Another idea: we can use a stack to keep the elements that we are going to keep, and we pop when the current element is less than the top (if we are trying to maximize the sum) but note: we are allowed to pop any time.

    # Actually, we can use a greedy algorithm: we traverse the array and maintain a stack. We push the current element if it is positive or if it is negative but we are going to keep it because the sum would be better? 

    # Alternatively, we can use a DP where dp[i] is the maximum sum we can have after processing the first i elements.

    # But note: N can be up to 200000.

    # We need an efficient solution.

    # Insight: The problem is equivalent to: we can choose a subsequence (not necessarily contiguous) of the array, but the subsequence must be a suffix of the original array? Actually, no: the kept sequence is the sequence of appended elements that are not popped, and we can pop arbitrarily from the end. But note: we can only pop the last element, so the kept sequence must be a contiguous sequence from the beginning? 

    # Actually, no: as shown above, we can skip elements arbitrarily from the end. But note: we can only pop the last element, so the kept sequence is the sequence of appended elements that are not popped, and the order is the original order. However, we can also pop an element that was appended earlier, and then append more. The kept sequence is the last k elements that were appended (without gaps) because if you pop an element, then the next appends are added to the end. 

    # Actually, the kept sequence is the sequence of appended elements that are not popped, and the order is the original order. But note: we can pop an element that was appended at an earlier index, and then we can append more. The kept sequence is not necessarily contiguous in the original array, but it is a subsequence that is a suffix of the appended elements? 

    # Let me reframe: We are allowed to do two operations at each step. We can think of the entire process as: we are going to choose a set of indices to append (and the rest we pop). But note: we cannot pop an element that was not appended. And we can only pop the last element. 

    # The key is: the kept sequence must be a contiguous sequence from the original array? Actually, no: as shown above.

    # However, note: the operations are sequential and we can only pop the last element. Therefore, the kept sequence is the sequence of appended elements that are not popped, and the order is the original order. But we can only pop the last element, so if we want to keep an element that is not at the end, we must not pop it until we are done with the rest. 

    # Actually, the kept sequence is the sequence of appended elements that are not popped, and the order is the original order. But we can only pop the last element, so the kept sequence must be a contiguous sequence from the beginning? 

    # Let me try with [1, 2, 3, 4, 5] and we want to keep [1,3,5]. 

    # Operation 1: append 1 -> [1]
    # Operation 2: append 2 -> [1,2]
    # Operation 3: