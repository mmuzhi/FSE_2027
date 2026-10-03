import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    M_val = int(data[1])
    intervals = []
    index = 2
    for i in range(n):
        L_i = int(data[index]); R_i = int(data[index+1]); index += 2
        intervals.append((L_i, R_i))
    
    base = [10**18] * (M_val+1)
    for (L_i, R_i) in intervals:
        if R_i < base[L_i]:
            base[L_i] = R_i
            
    R_min_arr = [10**18] * (M_val+1)
    if M_val >= 1:
        R_min_arr[M_val] = base[M_val]
    for i in range(M_val-1, 0, -1):
        R_min_arr[i] = base[i] if base[i] < R_min_arr[i+1] else R_min_arr[i+1]
        
    total_valid = 0
    for l in range(1, M_val+1):
        total_r = M_val - l + 1
        if R_min_arr[l] == 10**18:
            total_valid += total_r
        else:
            low_bound = max(l, R_min_arr[l])
            if low_bound > M_val:
                invalid_count = 0
            else:
                invalid_count = M_val - low_bound + 1
            total_valid += (total_r - invalid_count)
            
    print(total_valid)

if __name__ == "__main__":
    main()