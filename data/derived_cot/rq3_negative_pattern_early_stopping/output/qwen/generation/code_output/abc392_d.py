import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    dice = []
    index = 1
    for i in range(n):
        k = int(data[index]); index += 1
        faces = list(map(int, data[index:index+k]))
        index += k
        # Build frequency dictionary for this die
        from collections import defaultdict
        freq = defaultdict(int)
        for num in faces:
            freq[num] += 1
        dice.append((k, freq))
    
    # Now, we have dice as a list of (K_i, frequency_dict)
    # We'll consider all pairs (i, j) with i < j
    max_prob = 0.0
    for i in range(n):
        k_i, freq_i = dice[i]
        for j in range(i+1, n):
            k_j, freq_j = dice[j]
            # Find common numbers
            # We can take the keys of freq_i and freq_j and find intersection, but we can also iterate over the smaller one?
            # Alternatively, we can use set operations, but note: the keys might be large, but the total distinct numbers per die is at most the number of faces (which is <= 10^5) but we have only 100 dice, so we can do:
            # Let's get the common numbers by iterating over the keys of the smaller dictionary?
            # But we can do: common_keys = set(freq_i.keys()) & set(freq_j.keys())
            # But building sets for each pair might be heavy if the dictionaries are large. Alternatively, we can use the fact that the total distinct numbers is bounded by the total faces (10^5) but we have 100 dice, so the distinct numbers per die might be up to 10^5, but the total distinct numbers across dice is 10^5, so the distinct numbers per die might be large but the common numbers might be few.

            # Alternatively, we can iterate over the keys of one die and check if in the other, but that is O(distinct_i + distinct_j) which is acceptable because the distinct numbers per die is at most 10^5, but 10^5 * 4950 is 495e6 which is too many.

            # We need to optimize: Instead, we can precompute the distinct numbers for each die and then use a list of distinct numbers for each die, but then we have to check for each distinct number in die i if it is in die j.

            # But note: the total distinct numbers across all dice is at most 10^5 (since the numbers are from 1 to 10^5, but we don't know if they are consecutive). Actually, the numbers are integers from 1 to 10^5, so the distinct numbers in a die are a subset of [1, 10^5]. 

            # We can use a global set of numbers that appear in any die? But we don't need that.

            # Alternatively, we can precompute a list of distinct numbers for each die, and then for each pair, we can iterate over the distinct numbers of the first die and check if in the second die. But worst-case, if a die has 10^5 distinct numbers, then for each pair we do 10^5 checks, and 4950 * 10^5 = 495e6, which is acceptable in C++ but in Python might be borderline.

            # But note: the total faces is 10^5, so the distinct numbers per die cannot exceed 10^5, but the total distinct numbers across all dice is at most 10^5 (because the numbers are from 1 to 10^5, and we have 10^5 total faces, so the distinct numbers overall is at most 10^5). 

            # Actually, the input says: "K_1 + K_2 + ... + K_N <= 10^5", so the total faces is 10^5, so the distinct numbers per die can be at most 10^5, but the total distinct numbers across all dice is at most 10^5 (since the numbers are from 1 to 10^5, and we have 10^5 faces, so we can have at most 10^5 distinct numbers).

            # Therefore, the distinct numbers per die is at most 10^5, but the total distinct numbers is 10^5, so the distinct numbers per die might be large, but the common numbers between two dice might be small.

            # However, worst-case, two dice could have the same set