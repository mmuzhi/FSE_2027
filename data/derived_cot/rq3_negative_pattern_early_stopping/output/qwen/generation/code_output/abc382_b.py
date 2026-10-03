def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data:
        return
    parts = data[0].split()
    N = int(parts[0])
    D = int(parts[1])
    S = data[1].strip()
    
    # Extract indices of '@'
    indices = [i for i, char in enumerate(S) if char == '@']
    # Sort in descending order and take the first D
    indices.sort(reverse=True)
    remove_set = set(indices[:D])
    
    result_chars = []
    for i, char in enumerate(S):
        if char == '@' and i in remove_set:
            result_chars.append('.')
        else:
            result_chars.append(char)
            
    print(''.join(result_chars))

if __name__ == "__main__":
    main()