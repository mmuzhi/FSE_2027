import math

def main():
    import sys
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        K = int(data[index]); index += 1
        S_x = int(data[index]); index += 1
        S_y = int(data[index]); index += 1
        T_x = int(data[index]); index += 1
        T_y = int(data[index]); index += 1
        
        # Function to convert a coordinate to the base index and the offset for same parity (type A) or different parity (type B)
        # But note: we don't know the type. However, the tile is determined by the grid.

        # Instead, we can compute the tile indices for the start and target by considering the two types.

        # However, note: the problem is symmetric in x and y? Actually, the two types are swapped.

        # Let's define a function to map a coordinate to the tile index (i, j, k) for the same parity type and for the different parity type.

        # But note: the entire plane is covered by two types. We can compute:

        # For a point (x, y), we can compute:
        #   For same parity: 
        #       i = floor(x / K)
        #       Then, we need to find j and k such that j*K + k <= y < j*K + k+1. But note: the same parity condition requires that i and j have the same parity.

        #   But wait, the tile (i, j, k) for same parity is defined by i and j having the same parity. So if we compute i from x, then j must be chosen such that j has the same parity as i and then k is determined by y.

        # However, note: the entire y-axis is partitioned by the same parity tiles. Actually, the same parity tiles are arranged in a grid of size (infinite) x (infinite) with step K in x and step 1 in y (but with base j*K). 

        # Alternatively, we can compute the tile index by:

        #   Let i1 = floor(x / K)   [for same parity]
        #   Then, the x part is fixed. Then, we can compute j1 = floor((y) / K)   [but then the y part is broken by multiples of K, and then the offset k is from 0 to K-1]. However, the condition for same parity is that the y part is [j1*K + k, j1*K + k+1). 

        #   Actually, we can compute k1 = floor((y - j1*K) * K) ??? 

        #   But note: the y part for same parity is broken by multiples of K and then by integers. Actually, the entire y-axis is broken by lines at multiples of K and then every integer? 

        #   Actually, the same parity tile (i1, j1, k1) covers y in [j1*K + k1, j1*K + k1+1). So we can compute:
        #       j1 = floor(y / K)   [then the base is j1*K, and then the fractional part in y is (y - j1*K). Then k1 = floor((y - j1*K) * K) ??? 

        #   But note: the condition is j1*K + k1 <= y < j1*K + k1+1. Then k1 = floor((y - j1*K) * K) is not correct because (y - j1*K) might be fractional and then multiplied by K and floored, but note: the interval is of length 1, so we can compute:

        #       k1 = floor((y - j1*K) * K)   [but then the interval is [j1*K + k1, j1*K + k1+1) and k1 must be an integer between 0 and K-1.

        #   However, note: j1*K + k1 <= y < j1*K + k1+1  => k1 <= y - j1*K < k1+1  => k1 = floor(y - j1*K)   [but then k1 must be an integer and we require 0<=k1<K]. But note: y - j1*K is in [0, K) because j1 = floor(y/K) so y < (j1+1)*K, so y - j1*K < K. Then k1 = floor(y - j1*K) is an integer in [0, K-1] because y - j1*K is in [0, K). 

        #   But wait, the condition for same