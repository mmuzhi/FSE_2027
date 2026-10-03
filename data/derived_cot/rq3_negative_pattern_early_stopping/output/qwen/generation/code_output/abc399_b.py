def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    scores = list(map(int, data[1:1+n]))
    
    # Create list of (score, index)
    indexed_scores = [(score, i) for i, score in enumerate(scores)]
    
    # Sort in descending order
    indexed_scores.sort(key=lambda x: x[0], reverse=True)
    
    # We'll traverse and assign ranks
    r = 1
    # We'll use a list to store the rank for each original index
    result = [0] * n
    
    # Traverse the sorted list
    i = 0
    while i < n:
        # Count the number of same scores
        j = i
        while j < n and indexed_scores[j][0] == indexed_scores[i][0]:
            j += 1
        count = j - i
        # Assign the current rank r to all these count of people
        for idx in range(i, j):
            original_index = indexed_scores[idx][1]
            result[original_index] = r
        # Update r: add the count
        r += count
        i = j  # move to the next distinct score
    
    # Now, output each rank in the order of person 1 to N (i.e., index 0 to n-1)
    for rank in result:
        print(rank)

if __name__ == "__main__":
    main()