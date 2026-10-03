import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    
    n, q = map(int, data[0].split())
    s = list(data[1].strip())
    queries = []
    for i in range(2, 2+q):
        parts = data[i].split()
        if len(parts) < 2:
            continue
        x = int(parts[0])
        c = parts[1].strip()
        queries.append((x, c))
        
    # Precompute initial total count of "ABC"
    total = 0
    for i in range(n-2):
        if s[i] == 'A' and s[i+1] == 'B' and s[i+2] == 'C':
            total += 1
            
    # We'll maintain the string as a list of characters
    # For each query, update the character and adjust the total by checking the three triplets (if they exist)
    out_lines = []
    for query in queries:
        x, c = query
        pos = x - 1  # 0-indexed position
        
        # The triplets that are affected are those starting at indices: pos-2, pos-1, pos (if they are in the range [0, n-3])
        indices_to_check = set()
        if pos-2 >= 0 and pos-2 <= n-3:
            indices_to_check.add(pos-2)
        if pos-1 >= 0 and pos-1 <= n-3:
            indices_to_check.add(pos-1)
        if pos >= 0 and pos <= n-3:
            indices_to_check.add(pos)
            
        # Before updating, for each index i in indices_to_check, if the triplet starting at i is "ABC", then we remove it from total.
        for i in indices_to_check:
            # The triplet starting at i is s[i], s[i+1], s[i+2]
            if s[i] == 'A' and s[i+1] == 'B' and s[i+2] == 'C':
                total -= 1
                
        # Update the character at pos
        s[pos] = c
        
        # After updating, check the same indices and add if they are "ABC"
        for i in indices_to_check:
            if s[i] == 'A' and s[i+1] == 'B' and s[i+2] == 'C':
                total += 1
                
        out_lines.append(str(total))
        
    # Output each answer on a new line
    print("\n".join(out_lines))

if __name__ == "__main__":
    main()