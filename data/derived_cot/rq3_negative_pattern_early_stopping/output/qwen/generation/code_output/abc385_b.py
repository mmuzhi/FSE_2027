def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    
    # Parse first line
    first_line = data[0].split()
    H = int(first_line[0])
    W = int(first_line[1])
    X = int(first_line[2])
    Y = int(first_line[3])
    grid = []
    for i in range(1, 1+H):
        grid.append(data[i].strip())
    
    T = data[1+H].strip()
    
    # Convert starting position to 0-indexed
    x = X - 1
    y = Y - 1
    
    # We'll create a set for visited houses (cells with '@')
    visited_houses = set()
    # We also need to mark the starting cell? But note: the starting cell is '.' so no house.
    # However, we must note: if we move to a house, we mark it. Also, if we pass through a house (i.e., step on it) then we mark it.

    # But note: the problem says "distinct houses that he passed through or arrived at". 
    # We are going to simulate step by step and mark every '@' cell we step on (if we haven't seen it before) and then at the end, the count is the size of the set.

    # However, note: we might step on the same house multiple times, but we only count once.

    # We'll simulate the string T character by character.
    # We also need to update the current position and check the next cell for passability.

    # Directions mapping for moves
    moves = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }
    
    # We'll traverse each character in T
    for char in T:
        dx, dy = moves[char]
        nx, ny = x + dx, y + dy
        
        # Check if the next cell is within bounds and passable (not '#') and then update if it is passable (either '.' or '@')
        if 0 <= nx < H and 0 <= ny < W and grid[nx][ny] != '#':
            x, y = nx, ny
            # If the cell we moved to is '@', then we add it to visited_houses (if not already present)
            if grid[nx][ny] == '@':
                visited_houses.add((nx, ny))
        # Otherwise, we don't move and do nothing (the cell remains the same)
    
    # Now, we need to output the final position (converted back to 1-indexed) and the count of distinct houses.
    # The final position: (x+1, y+1) because we are 0-indexed.
    # But note: the problem says "Print X,Y,C in this order separated by spaces."
    # However, note: the grid boundaries are fixed, and we might have moved to a house that was already visited, but we only count distinct ones.

    # But wait: what if the starting cell is a house? The problem states S_{X,Y} is '.' so we don't have to worry.

    # However, note: the problem says "distinct houses that he passed through or arrived at during his actions". 
    # This includes the starting cell if it were a house? But it's not. And during the actions, we mark every '@' cell we step on.

    # But note: the sample input 1: 
    #   He starts at (3,4) which is '.' and then moves to (3,3) which is '@' -> so that house is marked.
    #   Then he moves to (3,2) which is '.' and then stays because (3,1) is blocked. Then moves to (4,2) which is '.' then to (4,3) which is '.' then to (3,3) which is '@' (already visited) then to (2,3) which is '.'.

    # So the distinct houses set has one element.

    # Therefore, we output:
    #   (x+1, y+1, len(visited_houses))

    print(f"{x+1} {y+1} {len(visited_houses)}")

if __name__ == "__main__":
    main()