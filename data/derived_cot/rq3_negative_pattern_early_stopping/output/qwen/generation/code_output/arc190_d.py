import sys
from itertools import product

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    p = int(data[1])
    A = []
    index = 2
    for i in range(n):
        row = list(map(int, data[index:index+n]))
        index += n
        A.append(row)
        
    # Count the number of zeros and their positions
    zeros = []
    for i in range(n):
        for j in range(n):
            if A[i][j] == 0:
                zeros.append((i, j))
                
    m = len(zeros)
    
    # We are going to consider the generating function for each zero independently.
    # The idea is to use the fact that the sum over all B of B^p can be broken down by the positions of zeros.
    # However, note that the exponentiation is non-linear. But we can use the linearity of the trace or other linear functionals?
    # Alternatively, we can use the concept of matrix calculus and generating functions.
    # But note: the problem asks for the entire matrix, so we need to compute each entry.
    # We can use the idea of "differentiating" the matrix power with respect to each zero and then setting the derivative to (p-1) choices.
    # Actually, we can use the following:
    # Let F(B) = B^p. Then the sum over all B is the same as the sum over all assignments to zeros of F(B).
    # We can use the fact that the sum over all assignments is the product over zeros of (sum_{x=1}^{p-1} x) for the linear part? But wait, the matrix power is not separable.

    # Another idea: use the binomial expansion for the matrix power? But that requires commuting matrices.

    # Alternatively, we can use the generating function for the entire matrix. But that is too heavy.

    # Let me think differently: the problem is to compute the sum of B^p for all B that are A with zeros replaced by numbers from 1 to p-1.
    # We can use the linearity of the matrix power? Actually, no. But note that the matrix power can be expressed as a polynomial in B.

    # However, we can use the concept of "generating the matrix power by the positions of zeros". But that is too vague.

    # Let me look for patterns in the sample outputs.

    # Sample Input 1: 
    #   N=2, p=3, A = [[0,1],[0,2]]
    #   Output: [[0,2],[1,2]]

    # Sample Input 2:
    #   N=3, p=2, A = [[1,0,0],[0,1,0],[0,0,1]]
    #   Output: [[1,1,1],[1,1,1],[1,1,1]]

    # In Sample Input 2, the matrix B is the identity matrix (since zeros are replaced by 1). Then B^2 is [[2,0,0],[0,2,0],[0,0,2]] but then mod 2 is [[0,0,0],[0,0,0],[0,0,0]]? But the sample output is [[1,1,1],[1,1,1],[1,1,1]].

    # Wait, actually, the sample input 2 says:
    #   "B^p for all possible B are as follows:
    #    - \begin{pmatrix}1&1&1 \\ 1&1&1 \\ 1&1&1\end{pmatrix}^2=\begin{pmatrix}3&3&3\\3&3&3\\3&3&3\end{pmatrix}"

    # So the matrix B is all ones. Then B^2 is a matrix with 3's on every entry. Then the sum (there is only one B) is that matrix. Then modulo 2, 3 mod 2 is 1. So each entry is 1. So the output is a 3x3 matrix of ones.

    # So the sample input 2 is correct.

    # Now, how to solve it?

    # Observation: The sum over all B of B^p is a linear operation? Actually, no. But note that the set of all B is a product space. We can use the fact that the matrix multiplication is linear in each row and column.

    # Alternatively, we can use the idea of "independent choices" for each zero. But the matrix power is a product of p matrices (each B). But that is too heavy.

    # Another idea: use the concept of "generating the matrix