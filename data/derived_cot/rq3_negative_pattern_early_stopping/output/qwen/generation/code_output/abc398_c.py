from collections import defaultdict

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # Count frequency
    freq = defaultdict(int)
    for num in A:
        freq[num] += 1
        
    # Find the candidate numbers (those with frequency 1)
    candidates = []
    for i, num in enumerate(A):
        if freq[num] == 1:
            candidates.append((num, i+1))  # store (value, label)
            
    if not candidates:
        print(-1)
    else:
        # Find the candidate with the maximum value
        max_val = max(candidate[0] for candidate in candidates)
        # There might be multiple candidates with the same max_val? But note: if a number is unique, then it appears once. But if two different numbers are the same? Then they are duplicates and not included. So the maximum value is unique in the candidate set? Not necessarily: two different numbers can be the same? No, because we are storing the value. But wait: two different numbers cannot be the same. So the maximum value is unique. However, we must find the label of the candidate that has that maximum value. But note: there might be multiple occurrences of the same maximum value? No, because if the maximum value appears more than once, then it wouldn't be in the candidate set (since frequency would be more than 1). So we can just take the first candidate with that value? But note: the condition is that the candidate set only includes numbers that appear once. So the maximum value appears once. But we must output the label of the person who has that value. However, the same value might appear in multiple places? No, because if it appears once, then there is only one occurrence.

        # But wait: what if the maximum value appears in the candidate set, but there are multiple candidates with the same value? Actually, no: because the candidate set is built from the array, and if a value appears once, then we add one candidate for that value. But note: the same value might appear again? No, because we are iterating and checking frequency. But wait: the frequency is counted for the entire array. So if a value appears once, then we add the candidate for every occurrence? Actually, no: we are iterating and checking the frequency of the current number. But if the frequency is 1, then we add the candidate. But if the same number appears again, then its frequency would be more than 1 and we skip. So we are adding one candidate per occurrence of a unique number.

        # However, note: the condition for being a candidate is that the number is unique. So we are adding every occurrence of a unique number. But if a number is unique, then there is exactly one occurrence. So we are adding one candidate per unique number.

        # Now, we want the candidate with the maximum value. But note: there might be multiple candidates with the same maximum value? No, because the maximum value is unique (since it's the maximum and the candidate set only has numbers that appear once). But wait: two different numbers can have the same value? No, because they are the same number. So we can simply find the candidate with the maximum value and then output its label.

        # However, we must be cautious: the candidate set might have multiple entries for the same value? No, because if a value appears once, then we add one candidate for that value. But if the same value appears again, then it wouldn't be added. So the candidate set has one candidate per unique number.

        # But wait: what if two different numbers are the same? Then they are duplicates and not included. So the candidate set has distinct numbers.

        # So we can do:
        #   max_val = max(num for num, count in freq.items() if count == 1)
        #   Then, we need to find the index (label) of the occurrence of max_val in the original array.

        # However, note: the candidate set we built is from the original array. We can also do:

        # Let's change: we don't need to store all candidates. We can do:
        #   max_val = -1
        #   candidate_label = -1
        #   for i, num in enumerate(A):
        #       if freq[num] == 1 and num > max_val:
        #           max_val = num
        #           candidate_label = i+1

        # But wait: what if there are two numbers with the same maximum value? Then we would update candidate_label to the last occurrence. But note: the maximum value is unique (because if two different numbers are the same, then they are duplicates and not included). So we can do that.

        # Alternatively, we can do: