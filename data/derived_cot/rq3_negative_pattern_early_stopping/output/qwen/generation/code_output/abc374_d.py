import math

def main():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    S_val = int(data[1])
    T_val = int(data[2])
    
    # Parse the next 4*n integers
    points = []
    index = 3
    for i in range(n):
        a = int(data[index]); b = int(data[index+1]); c = int(data[index+2]); d = int(data[index+3])
        index += 4
        points.append((a, b))
        points.append((c, d))
    
    # Build the nodes list: [ (0,0) ] + points
    nodes = [(0, 0)] + points
    total_nodes = 1 + 2*n  # indices 0 to 2*n
    
    # Precompute segment lengths and endpoints
    segment_length = [0] * n
    endpoints = [[] for _ in range(n)]
    for i in range(n):
        # endpoints[i] = [2*i+1, 2*i+2] (the two endpoints in the nodes list)
        p1 = nodes[2*i+1]
        p2 = nodes[2*i+2]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        segment_length[i] = math.sqrt(dx*dx + dy*dy)
        endpoints[i] = [2*i+1, 2*i+2]
    
    # Precompute distance matrix for all nodes (0 to total_nodes-1)
    dist_matrix = [[0.0] * total_nodes for _ in range(total_nodes)]
    for i in range(total_nodes):
        for j in range(total_nodes):
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            dx = x2 - x1
            dy = y2 - y1
            dist_matrix[i][j] = math.sqrt(dx*dx + dy*dy)
    
    # DP table: dp[mask][node_index]
    # mask: 0 to (1<<n)-1
    num_masks = 1 << n
    dp = [[10**18] * total_nodes for _ in range(num_masks)]
    dp[0][0] = 0.0
    
    # Iterate over all masks
    for mask in range(num_masks):
        for node_index in range(total_nodes):
            if dp[mask][node_index] == 10**18:
                continue
            # Try to print each segment not yet printed
            for i in range(n):
                if mask & (1 << i):
                    continue
                # For each endpoint of segment i
                for j in endpoints[i]:
                    # j is the index of the chosen starting endpoint (one of the two endpoints of segment i)
                    # The other endpoint is k
                    if j == endpoints[i][0]:
                        k = endpoints[i][1]
                    else:
                        k = endpoints[i][0]
                    
                    # Free movement from current node (node_index) to j
                    d_free = dist_matrix[node_index][j]
                    time_free = d_free / S_val
                    
                    # Printing time for segment i
                    time_print = segment_length[i] / T_val
                    
                    new_mask = mask | (1 << i)
                    new_time = dp[mask][node_index] + time_free + time_print
                    if new_time < dp[new_mask][k]:
                        dp[new_mask][k] = new_time
    
    # The answer is the minimum time over all masks (all segments printed) and all nodes
    ans = min(dp[(1<<n)-1])
    print("{:.15f}".format(ans))

if __name__ == '__main__':
    main()