import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    # Build prefix sum array
    P = [0]*(n+1)
    for i in range(1, n+1):
        P[i] = P[i-1] + A[i-1]
    
    # We are going to use the idea: 
    # Let F(x) = (x mod m) but we cannot simply use the prefix mod because the mod operation is not linear in the way we need for subtraction.

    # Instead, we can use the following:
    # We want to compute: 
    #   Sum_{l=1}^{n} Sum_{r=l}^{n} ( (P[r] - P[l-1]) mod m )
    #
    # We can break the mod operation: 
    #   (P[r] - P[l-1]) mod m = (P[r] mod m - P[l-1] mod m) mod m
    # But note: (a - b) mod m = (a - b + m) % m if a < b then we add m to make it positive.
    #
    # However, we can also think of the entire sum without mod and then subtract the multiples of m? But that is complicated.

    # Another idea: use the concept of "carry-over" from the mod operation. We can use a two-pointer or a binary search to count the number of subarrays that have a certain mod value? But note: we are summing the mod values, not counting.

    # Alternatively, we can use the following:
    #   Let X = P[r] mod m, and Y = P[l-1] mod m. Then the value for the subarray is (X - Y) mod m.
    #   But note: (X - Y) mod m = (X - Y + m) % m if X < Y, otherwise (X - Y) if X>=Y.
    #
    # We can split the sum into two parts:
    #   Sum_{l=1}^{n} Sum_{r=l}^{n} [ (P[r] - P[l-1]) mod m ]
    #   = Sum_{l=1}^{n} Sum_{r=l}^{n} [ (P[r] mod m - P[l-1] mod m + m) % m ]   [but this is not linear]

    # Actually, we can use the following trick:
    #   Let B[i] = P[i] % m. Then the value for subarray [l, r] is (B[r] - B[l-1]) % m, but note: the prefix sums are increasing, so P[r] >= P[l-1]. However, when modded, it might wrap around.

    # But note: the mod operation is not monotonic. However, we can use the fact that the prefix sums are increasing and the mod operation is periodic.

    # We can use a Fenwick tree or segment tree to count the number of prefix sums (mod m) in a certain range? 

    # Let's reframe: 
    #   We want to compute: 
    #       S = Sum_{l=0}^{n-1} Sum_{r=l}^{n-1} ( (P[r+1] - P[l]) mod m )
    #
    #   But note: P[0] = 0, and we consider l from 0 to n-1, and r from l to n-1 (so subarray from l+1 to r+1? Actually, we can index from 0 to n for P, and then the subarray [l, r] corresponds to P[r] - P[l-1]. But let's redefine: 
    #   Let Q[i] = P[i] % m for i from 0 to n.
    #
    #   Then the subarray [l, r] (with l from 1 to n, r from l to n) corresponds to (P[r] - P[l-1]) mod m.
    #
    #   We can write: 
    #       (P[r] - P[l-1]) mod m = (Q[r] - Q[l-1]) mod m
    #
    #   But note: because P[r] >= P[l-1] (since prefix sums are non-decreasing) then (P[r] - P[l-1]) mod m is not necessarily (Q[r] - Q[l-1]) mod m because if Q[r] < Q[l-1] then we have to add m. However, note that the prefix sums are increasing, but when modded, if the prefix