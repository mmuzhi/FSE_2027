import sys

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        n = int(data[index]); index += 1
        A = list(map(int, data[index:index+n]))
        index += n
        
        total = sum(A)
        # We are going to check if there exists a non-decreasing sequence with the same total.
        # But note: the operations preserve the total, so the target sequence must have the same total.
        # However, the operations are constrained: we can only move from right to left.
        # Therefore, we can only form a non-decreasing sequence if the following holds:
        #   For each k from 0 to n-1, the cumulative sum of the first k+1 elements in the target sequence must be at least the cumulative sum of the first k+1 elements in the original array? 
        # Actually, we can only move from right to left, so the left part can be increased by the right part. But the right part cannot be increased by the left part.
        # We can use a greedy algorithm to form the target sequence: we want to form the non-decreasing sequence with the same total.

        # Alternatively, we can use the following known fact: 
        #   The necessary and sufficient condition is that the total sum is the same and the sequence of prefix sums of the original array (when sorted in a particular way) must satisfy some condition.

        # Actually, note: we can rearrange the array arbitrarily? No, because we can only move from right to left. But we can assign the entire array arbitrarily as long as the total sum is fixed? 
        # Let's think: we can move from the right to the left arbitrarily, so we can assign the entire array arbitrarily. Therefore, the only condition is that the total sum is the same and the non-decreasing sequence must have the same total.

        # But wait, the sample [9,0] has total 9. The non-decreasing sequence must be [x, 9-x] with x<=9-x -> x<=4.5. Since x must be integer, x<=4. But we start with [9,0]. We cannot move from the left to the right, so we cannot decrease the left element. Therefore, we cannot get a non-decreasing sequence.

        # So the condition is not just the total sum. 

        # We can use the following idea: 
        #   We can only move from the right to the left. Therefore, the value at each index i in the target sequence must be at least the minimum value that can be achieved at that index, which is the original value at that index minus the amount that can be taken from the right. But note, we can take from the right arbitrarily, so the only constraint is that the target sequence must be non-decreasing and the total sum is fixed.

        # However, the problem is equivalent to: we can only decrease an element by transferring to the left, and we can only increase an element by transferring from the right. Therefore, the target sequence must satisfy:
        #   For each i, the value at i must be at least the original value at i minus the total amount that can be taken from the right (which is the entire array's total minus the original value at i) but that is not linear.

        # Another idea: 
        #   We can simulate the process from left to right. We want to assign the smallest possible value to the leftmost element, then the next, etc.

        # But note: we can only move from the right to the left. Therefore, the leftmost element can be set to any value as long as the rest of the array has the remaining total. However, we must also ensure that the sequence is non-decreasing.

        # Actually, we can use the following known solution for a similar problem (which is the "minimum operations to make the array non-decreasing" but with a fixed total and only right-to-left moves):

        # Step 1: Check if the total sum is the same (trivially, but the target sequence must have the same total).

        # Step 2: We can form a non-decreasing sequence if and only if the following holds:
        #   Let B be the target non-decreasing sequence (which we can choose arbitrarily as long as the total is fixed). We can choose B arbitrarily? Actually, we can assign the entire array arbitrarily (because we can move from right to left arbitrarily) as long as the total is fixed. But then, we can always form a non-decreasing sequence? 

        # However, the sample [9,0] shows that we cannot. Why? Because we cannot move from the left to the right. Therefore, the left element can only be increased by the right element, but the right element is 0