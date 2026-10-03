import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    H = list(map(int, data[1:1+n]))
    
    total_turns = 0
    for h in H:
        s = total_turns + 1
        low, high = 0, h
        while low < high:
            mid = (low + high) // 2
            # Calculate the damage for mid turns starting at turn s
            # The damage is: mid + 2 * ( (s+mid-1)//3 - (s-1)//3 )
            damage = mid + 2 * ((s + mid - 1) // 3 - (s - 1) // 3)
            if damage >= h:
                high = mid
            else:
                low = mid + 1
        total_turns += low
        
    print(total_turns)

if __name__ == "__main__":
    main()