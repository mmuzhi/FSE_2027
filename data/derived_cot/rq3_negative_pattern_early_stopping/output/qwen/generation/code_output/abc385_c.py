import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
    n = int(data[0])
    H = list(map(int, data[1:1+n]))
    
    # Group indices by height
    from collections import defaultdict
    groups = defaultdict(list)
    for idx, h in enumerate(H):
        groups[h].append(idx)
    
    ans = 1  # at least one building
    for height, indices in groups.items():
        indices.sort()
        if not indices:
            continue
        max_index = max(indices)
        used_set = set(indices)
        best_for_height = 1
        # For each starting index in the list
        for a in indices:
            # d from 1 to (max_index - a)
            # We can break early if d is too large such that a+d exceeds max_index, but we are iterating d from 1 to (max_index - a)
            for d in range(1, max_index - a + 1):
                count = 1
                next_val = a + d
                while next_val <= max_index and next_val in used_set:
                    count += 1
                    next_val += d
                if count > best_for_height:
                    best_for_height = count
        if best_for_height > ans:
            ans = best_for_height
    print(ans)

if __name__ == '__main__':
    main()