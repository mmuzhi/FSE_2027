import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    total_subarrays = n*(n+1)//2
    
    # Build dictionary of positions for each number
    pos_dict = {}
    for idx, num in enumerate(A):
        if num not in pos_dict:
            pos_dict[num] = []
        pos_dict[num].append(idx)
    
    # For numbers that do not appear, we don't need to consider (they contribute 0)
    # But the array values are from 1 to N, so we can also consider only the keys in pos_dict.
    ans = 0
    for num, positions in pos_dict.items():
        # positions is sorted by index
        gaps = []
        # Before the first occurrence
        if positions[0] > 0:
            gaps.append(positions[0])
        # Between occurrences
        for i in range(1, len(positions)):
            if positions[i] - positions[i-1] > 1:
                gaps.append(positions[i] - positions[i-1] - 1)
        # After the last occurrence
        if positions[-1] < n-1:
            gaps.append(n - 1 - positions[-1])
        
        gap_sum = 0
        for gap in gaps:
            gap_sum += gap*(gap+1)//2
        
        # The number of subarrays containing num is total_subarrays - gap_sum
        ans += (total_subarrays - gap_sum)
    
    print(ans)

if __name__ == "__main__":
    main()