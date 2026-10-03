import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    # Parse the first integer as N
    it = iter(data)
    N = int(next(it))
    # Read the next N*N numbers for the 3D array
    arr = [[[0]*(N) for _ in range(N)] for __ in range(N)]
    # We'll read the input in row-major order: first N rows, each row has N*N numbers? Actually, the input is given as:
    # N
    # Then N*N numbers: first N rows of the first N matrices? Actually, the input format is:
    # N
    # A_{1,1,1} A_{1,1,2} ... A_{1,1,N}
    # A_{1,2,1} A_{1,2,2} ... A_{1,2,N}
    # ...
    # A_{1,N,1} A_{1,N,2} ... A_{1,N,N}
    # A_{2,1,1} ... etc.

    # So the total numbers after N is N*N*N? Actually, no: the input has N*N*N numbers, but they are given in a specific order.

    # Actually, the input has N*N*N numbers, but they are given in row-major order for the first dimension? 

    # The input format: 
    #   First line: N
    #   Then, for x from 1 to N:
    #       for y from 1 to N:
    #           read N numbers for z from 1 to N: A_{x,y,1} to A_{x,y,N}

    # So we have N*N*N numbers.

    # We'll read all the numbers and then reshape.

    total_numbers = N*N*N
    numbers = [int(next(it)) for _ in range(total_numbers)]
    index = 0
    # We'll fill the 3D array: arr[x][y][z] for x,y,z from 0 to N-1.
    # The input order: first all x=0, then x=1, ... and for each x, all y from 0 to N-1, and for each y, all z from 0 to N-1.
    # But note: the sample input: 
    #   2
    #   1 2
    #   3 4
    #   5 6
    #   7 8
    # This is for N=2, and the array is:
    #   arr[0][0] = [1, 2]
    #   arr[0][1] = [3, 4]
    #   arr[1][0] = [5, 6]
    #   arr[1][1] = [7, 8]

    # But wait, the sample input has 8 numbers, and N=2, so 2*2*2=8.

    # We can fill the array by:
    #   for x in range(N):
    #       for y in range(N):
    #           for z in range(N):
    #               arr[x][y][z] = numbers[index]
    #               index += 1

    # But the input order is: 
    #   First row (x=0) has two rows (each row has two numbers): 
    #       first row: [1, 2] -> y=0: [1,2] and y=1: [3,4] for x=0.
    #   Then x=1: [5,6] for y=0 and [7,8] for y=1.

    # So the order is: 
    #   x=0, y=0, z=0 -> 1
    #   x=0, y=0, z=1 -> 2
    #   x=0, y=1, z=0 -> 3
    #   x=0, y=1, z=1 -> 4
    #   x=1, y=0, z=0 -> 5
    #   x=1, y=0, z=1 -> 6
    #   x=1, y=1, z=0 -> 7
    #   x=1, y=1, z=1 -> 8

    # So we can simply fill in row-major order.

    # But note: the sample input has the numbers in the order: 
    #   1 2 3 4 5 6 7 8

    # However, the sample input is given as:
    #   2
    #   1 2