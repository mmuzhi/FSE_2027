def compute_min_flips(s):
    if len(s) == 1:
        if s == '0':
            return (0, 1)
        else:
            return (1, 0)
    n = len(s)
    part_len = n // 3
    s1 = s[:part_len]
    s2 = s[part_len:2*part_len]
    s3 = s[2*part_len:]
    a1, b1 = compute_min_flips(s1)
    a2, b2 = compute_min_flips(s2)
    a3, b3 = compute_min_flips(s3)
    a = min(a1 + a2 + a3, a1 + a2 + b3, a1 + b2 + a3, b1 + a2 + a3)
    b = min(b1 + b2 + b3, b1 + b2 + a3, b1 + a2 + b3, a1 + b2 + b3)
    return (a, b)

def compute_initial_value(s):
    if len(s) == 1:
        return s
    n = len(s)
    part_len = n // 3
    s1 = s[:part_len]
    s2 = s[part_len:2*part_len]
    s3 = s[2*part_len:]
    v1 = compute_initial_value(s1)
    v2 = compute_initial_value(s2)
    v3 = compute_initial_value(s3)
    count1 = (v1 == '1') + (v2 == '1') + (v3 == '1')
    if count1 >= 2:
        return '1'
    else:
        return '0'

def main():
    import sys
    data = sys.stdin.read().splitlines()
    N = int(data[0])
    s = data[1].strip()
    # Compute the initial value of the root
    init_val = compute_initial_value(s)
    # Compute the minimal flips to set the root to 0 and 1
    a, b = compute_min_flips(s)
    if init_val == '1':
        print(a)
    else:
        print(b)

if __name__ == '__main__':
    main()