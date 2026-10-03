import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2+n]))
    B = list(map(int, data[2+n:2+n+m]))
    
    max_val = 200000
    min_index_arr = [10**9] * (max_val+1)  # 1-indexed up to max_val
    
    # We are going to index by the value of A_i (which is between 1 and max_val)
    # For each person i (from 0 to n-1), we have A[i] (which is the gourmet level of person i+1)
    for i in range(n):
        a_val = A[i]
        if a_val <= max_val:
            if i+1 < min_index_arr[a_val]:
                min_index_arr[a_val] = i+1
    
    # Now, build a prefix minimum array for values from 1 to max_val
    # But note: we want for each value v, the minimum index among all A_i <= v.
    # However, our min_index_arr[v] is the minimum index for A_i exactly equal to v.
    # Then, we want the minimum index for any A_i in [1, v].
    # We can do a forward pass: 
    #   Let prefix_min[i] = min(min_index_arr[1], min_index_arr[2], ... , min_index_arr[i])
    # But note: we only care about values from 1 to max_val.
    prefix_min = [10**9] * (max_val+1)
    current_min = 10**9
    for v in range(1, max_val+1):
        if min_index_arr[v] < current_min:
            current_min = min_index_arr[v]
        prefix_min[v] = current_min

    # Now, for each sushi j with deliciousness B_j, we look at prefix_min[B_j] (if B_j is within [1, max_val])
    # But note: B_j can be up to 200000, so we can use it directly.
    # However, if B_j is greater than max_val, we use max_val? But max_val is 200000 and B_j is up to 200000, so no problem.
    # But note: our prefix_min array is built for values from 1 to 200000.

    # But what if B_j is 0? The constraints say at least 1, so no problem.

    out_lines = []
    for b_val in B:
        if b_val > max_val:
            # Since our prefix_min is only up to max_val, and we built for 1..max_val, we can use the value at max_val if b_val>max_val?
            # But note: if b_val > max_val, then we consider all persons (since A_i are at most 200000). So we can use prefix_min[max_val]?
            # However, the problem says A_i and B_i are at least 1 and at most 200000, so b_val won't exceed 200000.
            candidate = prefix_min[max_val]
        else:
            candidate = prefix_min[b_val]
        
        if candidate > n:
            out_lines.append("-1")
        else:
            out_lines.append(str(candidate))
    
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()