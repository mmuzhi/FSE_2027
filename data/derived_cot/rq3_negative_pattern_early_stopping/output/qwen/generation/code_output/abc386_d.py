import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        print("Yes")
        return
    n, m = map(int, data[0].split())
    constraints = []
    for i in range(1, m+1):
        parts = data[i].split()
        x = int(parts[0])
        y = int(parts[1])
        c = parts[2]
        constraints.append((x, y, c))
    
    # We'll create two dictionaries for rows and columns to store the constraints.
    # For rows: we want to know the maximum j (for black) and minimum j (for white) for each row.
    # Similarly for columns.
    row_black_max = {}  # row: max column index that is black (or 0 if none)
    row_white_min = {}  # row: min column index that is white (or n+1 if none)
    col_black_max = {}  # col: max row index that is black (or 0 if none)
    col_white_min = {}  # col: min row index that is white (or n+1 if none)
    
    for (x, y, c) in constraints:
        if c == 'B':
            # For row x: update the maximum black column
            if x in row_black_max:
                if y > row_black_max[x]:
                    row_black_max[x] = y
            else:
                row_black_max[x] = y
            # For column y: update the maximum black row
            if y in col_black_max:
                if x > col_black_max[y]:
                    col_black_max[y] = x
            else:
                col_black_max[y] = x
        else:  # 'W'
            # For row x: update the minimum white column
            if x in row_white_min:
                if y < row_white_min[x]:
                    row_white_min[x] = y
            else:
                row_white_min[x] = y
            # For column y: update the minimum white row
            if y in col_white_min:
                if x < col_white_min[y]:
                    col_white_min[y] = x
            else:
                col_white_min[y] = x
                
    # Now, for each row and column, we can determine the valid range for a[i] and b[j].
    # For row i:
    #   a[i] must be at least row_black_max[i] (if exists) and less than row_white_min[i] (if exists).
    #   If there is no black cell, then row_black_max[i] doesn't exist -> we set to 0.
    #   If there is no white cell, then row_white_min[i] doesn't exist -> we set to n+1.
    #   Similarly for columns.
    
    # We'll create two arrays (or dictionaries) for the valid a[i] and b[j] ranges.
    # But note: n can be up to 10^9, so we cannot iterate over all rows and columns.
    # Instead, we will consider only the rows and columns that appear in the constraints, and also the rows and columns that are forced by the constraints to have a particular relation.
    
    # However, note: the condition must hold for every cell (i, j). But we are only given M constraints. 
    # But the condition is very strong: a[i] >= j  <=>  b[j] >= i for every (i, j).
    # This condition is equivalent to: 
    #   a[i] = max_{j} { j such that b[j] >= i }   (but note, we can also think of it as: the row i's split a[i] must be the maximum j such that b[j] >= i, and similarly b[j] must be the maximum i such that a[i] >= j).
    
    # Actually, the condition (a[i] >= j) == (b[j] >= i) for every (i, j) is equivalent to:
    #   a[i] = max{ j : b[j] >= i }   (for each row i, the split is the maximum column j for which the column j has b[j] >= i)
    #   and similarly, b[j] = max{ i : a[i] >= j }   (for each column j, the split is the maximum row i for which the row i has a[i] >= j)
    
    # But note: the condition is symmetric. Therefore, the grid is defined by a single sequence: 
    #   Let f(i) = max{ j : b[j] >= i }   and then b[j] = max{ i : a[i] >= j }.
    #   But also, a[i] = max{ j : b[j] >= i } = max{ j