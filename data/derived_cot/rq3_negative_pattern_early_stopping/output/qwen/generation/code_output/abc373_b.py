def main():
    S = input().strip()
    mapping = {}
    for idx, char in enumerate(S):
        mapping[char] = idx + 1
        
    letters = [chr(ord('A') + i) for i in range(26)]
    positions = [mapping[letter] for letter in letters]
    
    total_distance = 0
    for i in range(1, 26):
        total_distance += abs(positions[i] - positions[i-1])
        
    print(total_distance)

if __name__ == "__main__":
    main()