import sys

def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    index = 1
    results = []
    for _ in range(t):
        n = int(data[index]); index += 1
        constraints = []
        for i in range(n):
            a = int(data[index]); b = int(data[index+1]); c = int(data[index+2]); index += 3
            constraints.append((a, b, c))
        
        # If there are no constraints, then the condition is always true, so all positive integers (x,y) are valid.
        # But note: the problem says the number of pairs is finite, so there must be constraints? Actually, if n=0, then condition holds for all (x,y) but the problem says the number is finite, so n>=1 in practice? But the problem says "It can be proved that the number of such pairs of positive integers satisfying the condition is finite", so there must be at least one constraint? Actually, the condition is for all i, so if n=0, then the condition is vacuously true, but then the set of (x,y) is infinite. But the problem says the number is finite, so we assume n>=1.

        # However, the problem says: "You are given three length-N sequences", so n>=1.

        # We are to find the number of (x,y) such that for every constraint (a,b,c): a*x+b*y < c.

        # Step 1: Compute x_max = min_i floor((c-1)/a) for each constraint (a,b,c)
        x_max = None
        for a, b, c in constraints:
            # For this constraint, the maximum x is floor((c-1)/a)
            if x_max is None:
                x_max = (c-1) // a
            else:
                x_max = min(x_max, (c-1) // a)
        # But note: if x_max < 1, then there are no x, so answer=0.
        if x_max < 1:
            results.append("0")
            continue

        # Step 2: Compute the maximum k (which is the maximum y) is K_max = min_i floor((c-1)/b) for each constraint (a,b,c)
        K_max = None
        for a, b, c in constraints:
            if K_max is None:
                K_max = (c-1) // b
            else:
                K_max = min(K_max, (c-1) // b)
        # But note: k is the floor value for y, and we are going to iterate k from 1 to K_max.

        # However, note: the condition for k is: for every constraint (a,b,c), we require (c-1) >= k*b.
        # But K_max is the minimum over i of floor((c-1)/b), so k from 1 to K_max is valid.

        # But note: the condition for x in the definition of x_k is: for every constraint (a,b,c), x <= (c-1 - k*b) // a.
        # Then x_k = min_i ((c-1 - k*b) // a)

        # We want to compute: ans = 0
        # for k from 1 to K_max:
        #   x_k = min_i ((c-1 - k*b) // a)   [for each constraint (a,b,c)]
        #   if x_k < 1: break
        #   else: ans += x_k

        # But note: the total number of k is K_max, which can be up to 10^9, so we cannot iterate from 1 to K_max.

        # We need to find the ranges of k for which x_k is constant or changes.

        # Alternatively, we can use a different approach: iterate over k by breaking at the points where x_k changes.

        # But note: the total number of constraints is n (which is the number of lines in the test case), and the total n across test cases is 200000.

        # We can use a method to find the maximum k for which x_k >= 1, and then break when x_k < 1.

        # But K_max might be large (up to 10^9) and we cannot iterate over each k.

        # We need to find the values of k where x_k changes. The function x_k is the minimum over i of floor((c_i-1 - k*b_i)/a_i). 

        # For each constraint i, the function f_i(k) = floor((c_i-1 - k*b_i)/a_i) is a linear function in k (with slope -b