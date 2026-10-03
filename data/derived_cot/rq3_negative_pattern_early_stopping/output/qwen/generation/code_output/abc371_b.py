def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data:
        return
    
    first_line = data[0].split()
    n = int(first_line[0])
    m = int(first_line[1])
    
    has_first_male = [False] * (n + 1)
    
    output_lines = []
    for i in range(1, m + 1):
        parts = data[i].split()
        family = int(parts[0])
        gender = parts[1]
        
        if gender == 'M':
            if not has_first_male[family]:
                output_lines.append("Yes")
                has_first_male[family] = True
            else:
                output_lines.append("No")
        else:
            output_lines.append("No")
    
    for line in output_lines:
        print(line)

if __name__ == "__main__":
    main()