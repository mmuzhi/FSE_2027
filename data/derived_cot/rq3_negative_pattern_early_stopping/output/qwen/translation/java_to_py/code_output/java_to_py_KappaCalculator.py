def kappa(test_data, k):
    # Convert test_data to a matrix (list of lists)
    # We assume test_data is a list of lists of integers
    # k is the number of categories (size of the matrix)
    total_sum = 0
    P0 = 0.0
    # Calculate the diagonal sum (P0)
    for i in range(k):
        P0 += test_data[i][i]
    # Now, calculate row sums (xsum), column sums (ysum) and total_sum
    xsum = [0] * k
    ysum = [0] * k
    total_sum = 0
    for i in range(k):
        for j in range(k):
            xsum[i] += test_data[i][j]
            ysum[j] += test_data[i][j]
            total_sum += test_data[i][j]
    # Now, calculate Pe
    Pe = 0.0
    for i in range(k):
        Pe += ysum[i] * xsum[i]
    # Normalize Pe by total_sum^2
    Pe = Pe / (total_sum * total_sum)
    # Normalize P0 by total_sum
    P0 = P0 / total_sum
    # Return the kappa value
    return (P0 - Pe) / (1 - Pe)

def fleissKappa(test_data, N, k, n):
    # test_data: list of lists, each inner list is a subject's annotations
    # N: number of subjects
    # k: number of categories
    # n: number of annotations per subject (should be the same as the length of each row)
    P = [0.0] * N
    total_annotations = 0  # This will be the total number of annotations (across all subjects and categories)
    for i in range(N):
        row_sum = sum(test_data[i])
        # But note: the Java code uses a variable called 'sum' which is then used again. We'll use a different variable.
        # Calculate the sum of squares for this subject
        temp = 0.0
        for j in range(k):
            temp += test_data[i][j] * test_data[i][j]
        # Subtract n and divide by (n-1)*n
        temp -= n
        temp /= (n - 1) * n
        P[i] = temp
    # Calculate P0: average of P
    P0 = sum(P) / N
    # Now, calculate the column sums (pj) for each category
    # First, we need the total number of annotations (each annotation is a count in the matrix)
    # But note: the Java code uses a variable 'sum' that was accumulating the row sums for each subject. However, in the FleissKappa method, the variable 'sum' was used to accumulate the total annotations (across all subjects and categories). But wait, in the Java code, the variable 'sum' is declared outside the loop and then inside the loop they do:
    #   for (int i = 0; i < N; i++) {
    #       double temp = 0.0;
    #       for (int j = 0; j < k; j++) {
    #           sum += dataMat[i][j];
    #           temp += dataMat[i][j] * dataMat[i][j];
    #       }
    #   }
    # So they are accumulating the total annotations (each cell is an annotation count). But note: the matrix is count matrix, so each cell is the count of annotations in that category for that subject.
    # However, in our Python code, we didn't accumulate the total_annotations in the same way. We can recalculate the total_annotations by summing all the elements in test_data.
    # But note: the Java code uses the same variable 'sum' for two purposes: first for the row sums and then for the total. Actually, the Java code does:
    #   int sum = 0;
    #   for (int i = 0; i < N; i++) {
    #       for (int j = 0; j < k; j++) {
    #           sum += dataMat[i][j];
    #       }
    #   }
    #   ... and then uses it again in the calculation of Pe.
    # But wait, in the provided Java code for fleissKappa, the variable 'sum' is declared and then used in the inner loop to accumulate the row sums for each subject? Actually, no, the Java code for fleissKappa does not have that. Let me check:

    # The provided Java code for fleissKappa:
    #   double sum = 0.0;
    #   for (int i = 0; i < N; i++) {
    #       double temp = 0.0;
    #       for (int j = 0; j < k; j++) {
    #           sum += dataMat[i][j];
    #           temp += dataMat[i][j] * dataMat[i][j];
    #       }
    #       temp -= n;
    #       temp /= (n - 1) * n;
    #       P[i] = temp;
    #   }
    #   double P0 = Arrays.stream(P).sum() / N;
    #   double[] pj = new double[k];
    #   for (int j = 0; j < k; j++) {
    #       for (int i = 0; i < N; i++) {
    #           pj[j] += dataMat[i][j];
    #       }
    #       pj[j] /= sum;
    #   }
    #   double Pe = Arrays.stream(pj).map(p -> p * p).sum();

    # So the variable 'sum' is being used to accumulate the total number of annotations (each cell is an annotation). But note: the matrix is count matrix, so each cell is the count of annotations in that category for that subject.

    # In our Python code, we can calculate the total_annotations by summing all the elements in test_data.

    total_annotations = sum(sum(row) for row in test_data)
    pj = [0.0] * k
    for j in range(k):
        for i in range(N):
            pj[j] += test_data[i][j]
        pj[j] /= total_annotations
    Pe = sum(p * p for p in pj)
    return (P0 - Pe) / (1 - Pe)

# Example usage (if we want to run the main method, but note: the problem doesn't require a main method, just the two functions)
if __name__ == "__main__":
    # Example for kappa
    data1 = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]
    print(kappa(data1, 3))  # Expected: 0.25

    # Example for fleissKappa (using the provided example)
    data2 = [
        [0, 0, 0, 0, 14],
        [0, 2, 6, 4, 2],
        [0, 0, 3, 5, 6],
        [0, 3, 9, 2, 0],
        [2, 2, 8, 1, 1],
        [7, 7, 0, 0, 0],
        [3, 2, 6, 3, 0],
        [2, 5, 3, 2, 2],
        [6, 5, 2, 1, 0],
        [0, 2, 2, 3, 7]
    ]
    print(fleissKappa(data2, 10, 5, 14))