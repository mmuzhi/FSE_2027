import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    
    # We are going to compute the positions of each element (1-indexed element should be at 0-indexed position i-1)
    pos = [0] * (n+1)
    for i in range(n):
        pos[arr[i]] = i
        
    # We are going to consider the sorted array: [1, 2, ..., n]
    # We need to move each element to its target position (which is i-1 for element i).
    # But note: the minimal cost is the sum of the costs of the swaps. Each swap is uniquely identified by the left index at the time of swap.

    # Alternatively, we can use a known approach for such problems: 
    # We can consider that the minimal cost is the sum of the initial positions of the elements (if we consider 1-indexed) minus the sum of the target positions (which is 0-indexed) but that doesn't account for the cost structure.

    # Another known approach: 
    # We can consider that the cost is the sum of the indices (1-indexed) of the left element for every swap. 
    # We can also think: what is the minimal cost to bring the element 1 to the front? Then element 2 to the second, etc.

    # However, note: the problem is equivalent to: 
    # We have an array of the current positions of the numbers (for number i, its current position is pos[i]).
    # We want to move each number i to position i-1 (0-indexed). The cost of moving a number from position j to position i (if j>i) is the sum of the indices (1-indexed) of the swaps that move it left, but note that the swaps are adjacent and the left index changes.

    # Actually, there is a known solution for this problem: 
    # The answer is the sum_{i=1}^{n} (initial_position[i] - (i-1)) but that is the number of inversions? 

    # But wait, the sample: 
    # For [3,2,1]:
    #   Element1: initial position 2 (0-indexed), target 0 -> needs to move left by 2.
    #   Element2: initial position 1, target 1 -> 0 moves.
    #   Element3: initial position 0, target 2 -> needs to move right by 2.

    # But the cost is not the distance, but the indices of the swaps.

    # Insight from known similar problems (e.g., CodeForces problems) is that the minimal cost is the sum of the initial positions of the elements (if we consider 1-indexed) minus the sum of the target positions (which is the sum of 0 to n-1) but then adjusted for the fact that we can only swap adjacent elements and the cost is the left index.

    # Actually, consider: 
    # The total cost is the sum_{i=0}^{n-2} (the number of times we swap at position i) * (i+1) but that is not helpful.

    # Another known idea: 
    # We can consider that the minimal cost is the sum_{i=1}^{n} (initial_position[i] - (i-1)) but then we have to account for the fact that when an element moves, it shifts the positions of the other elements.

    # Actually, there is a known solution for this exact problem (from competitive programming). 

    # Let me recall: 
    # We can compute the cost by considering the positions of the elements and then subtract the "free" movements. 

    # Alternatively, we can use a greedy method that builds the sorted array from left to right and for each element, we move it to the front by swapping leftwards, and the cost for moving an element from position j to the front (if there are k elements between it and the front) is the sum of the indices (1-indexed) of the swaps, but note that the indices change as we move.

    # However, note: the problem is equivalent to: 
    # We have an array of the current positions of the numbers (for number i, its current position is pos[i]). 
    # We want to move each number i to position i-1. The cost to move a number from position j to position i (if j>i) is the sum_{k=i}^{j-1} (k+1) (if we move it left) but if we move it right, then the cost is the sum_{k=j}^{i-1} (k+1) (but note: moving right, the left index is