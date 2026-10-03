import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    p = list(map(int, data[1:1+n]))
    q = list(map(int, data[1+n:1+2*n]))
    
    # We'll create an array for the bib numbers (q) and use p as given.
    # We are going to create an array 'ans' for bib numbers from 1 to n.
    ans = [0] * (n+1)  # 1-indexed up to n
    
    # We traverse each person (from 0 to n-1)
    for i in range(n):
        # The current person's bib is q[i]
        bib_i = q[i]
        # The target natural number is p[i]
        target_natural = p[i]
        # The bib of the target is q[target_natural - 1] (because q is 0-indexed, and target_natural is between 1 and n)
        target_bib = q[target_natural-1]
        # Assign the answer for bib_i
        ans[bib_i] = target_bib
    
    # Now, we output the answers for bib numbers 1 to n
    # But note: the problem asks for S_1, S_2, ... S_n (for bib numbers 1 to n)
    # We have stored the answer for bib_i in ans[bib_i]. However, we must output in the order of bib numbers 1 to n.
    # But note: the array ans is indexed by bib number. So we can simply output ans[1], ans[2], ... ans[n].
    # However, what if a bib number is missing? The problem states that the bib numbers are distinct and from 1 to n, so every bib number from 1 to n appears exactly once in q.
    # But note: our ans array is built for the bib numbers that appear in q. However, we are building for every bib_i that appears, and the bib numbers are from 1 to n, so we have set ans[bib_i] for every bib_i in q.

    # But note: the array ans might have zeros for bib numbers that are not in q? But q has n distinct numbers from 1 to n, so we set every index from 1 to n? Actually, no: we set only the bib_i that appear in q. But q has all numbers from 1 to n? Not necessarily: the problem says the values of Q_i are distinct and between 1 and n, so yes, q contains each number from 1 to n exactly once.

    # Therefore, we can output from 1 to n.

    # However, note: the sample: 
    #   n=4, we set ans[2]=4, ans[3]=1, ans[1]=3, ans[4]=2.
    #   Then, output: 
    #       ans[1] = 3
    #       ans[2] = 4
    #       ans[3] = 1
    #       ans[4] = 2

    # So we output: 3 4 1 2

    # But wait, the problem says: "Print S_1, S_2, ..., S_N in this order", meaning for bib number 1, then 2, then 3, then 4.

    # So we output:
    result = []
    for i in range(1, n+1):
        result.append(str(ans[i]))
    
    print(" ".join(result))

if __name__ == "__main__":
    main()