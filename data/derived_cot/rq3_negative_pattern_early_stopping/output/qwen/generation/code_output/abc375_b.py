import math

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    points = []
    index = 1
    for i in range(n):
        x = int(data[index]); y = int(data[index+1]); index += 2
        points.append((x, y))
    
    total_cost = 0.0
    current_x, current_y = 0, 0
    
    for x, y in points:
        dx = x - current_x
        dy = y - current_y
        total_cost += math.sqrt(dx*dx + dy*dy)
        current_x, current_y = x, y
        
    dx = current_x - 0
    dy = current_y - 0
    total_cost += math.sqrt(dx*dx + dy*dy)
    
    print(total_cost)

if __name__ == "__main__":
    main()