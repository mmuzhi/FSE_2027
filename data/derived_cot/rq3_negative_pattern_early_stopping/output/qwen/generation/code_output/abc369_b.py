def main():
    import sys
    data = sys.stdin.read().splitlines()
    n = int(data[0])
    left_keys = []
    right_keys = []
    for i in range(1, n+1):
        parts = data[i].split()
        key = int(parts[0])
        hand = parts[1]
        if hand == 'L':
            left_keys.append(key)
        else:
            right_keys.append(key)
    
    # For each hand, we can choose the initial position arbitrarily, so we set the initial position to the first key in the sequence (if the sequence is non-empty) to minimize the first move.
    # Then the fatigue for that hand is the sum of absolute differences between consecutive keys in the sequence.
    # But note: if the sequence is empty, then the fatigue is 0.

    def calculate_fatigue(keys):
        if not keys:
            return 0
        total = 0
        # We start at the first key, so the first move is 0.
        # Then we move from keys[i] to keys[i+1] for each consecutive pair.
        for i in range(1, len(keys)):
            total += abs(keys[i] - keys[i-1])
        return total

    left_fatigue = calculate_fatigue(left_keys)
    right_fatigue = calculate_fatigue(right_keys)
    print(left_fatigue + right_fatigue)

if __name__ == "__main__":
    main()