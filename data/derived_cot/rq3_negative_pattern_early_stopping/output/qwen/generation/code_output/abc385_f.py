import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    buildings = []
    index = 1
    for i in range(n):
        x = int(data[index]); h = int(data[index+1]); index += 2
        buildings.append((x, h))
    
    # If there is only one building, then we need to check if from (0,0) we can see it.
    # But the condition: the line from (0,0) to (x, h) must not intersect any other building. There are none, so it is visible.
    # But the problem: we are to find the maximum height from which it is not possible to see all buildings. 
    # Since there is only one building, we can see it from any h>=0? Actually, no: the condition is that the line from (0, h) to (x, h) is not blocked by any other building (none). But wait, the building is at (x, h) — actually, the building is from (x,0) to (x, h). The line from (0, h) to (x, h) is horizontal. It will not intersect any building (since the building is at x, and the line is at y=h). But wait, the building is at x, so the line from (0, h) to (x, h) is at y=h. The building is from (x,0) to (x, h). The line segment from (0, h) to (x, h) ends at (x, h). The building is at x, so the line segment from (0, h) to (x, h) does not go through the building (it just touches at the top). But the condition is that the line segment does not intersect any other building. There are no other buildings, so it's visible. 

    # But wait, the problem says: "From a point P with coordinate x and height h, building i is considered visible if there exists a point Q on building i such that the line segment PQ does not intersect with any other building."

    # In the case of one building, we are at (0, h) and we look at the building (x, H). We can choose Q to be (x, H). The line segment from (0, h) to (x, H) must not intersect any other building (none). So it is visible.

    # But what if h is very high? Then the line from (0, h) to (x, H) is from (0, h) to (x, H). This line might go through the building? Actually, the building is at x, so the line segment from (0, h) to (x, H) is from (0, h) to (x, H). The building is the vertical segment at x from 0 to H. The line segment from (0, h) to (x, H) is a straight line. At x, the y-coordinate is H. So the line segment ends at the top of the building. There are no other buildings, so it is visible.

    # Therefore, for one building, we can always see it from any h>=0. Then the set of h from which we cannot see all buildings is empty. But the problem says: "Find the maximum height at coordinate 0 from which it is not possible to see all buildings." 

    # Since there is only one building, "all buildings" is just that one. So we can see it from any h>=0. Then the maximum height from which we cannot see all buildings does not exist? But the problem says "if it is possible to see all buildings from coordinate 0 and height 0, print -1". 

    # In the one-building case, from (0,0) we can see the building (because there are no other buildings to block). So we should output -1.

    # But wait, the condition for one building: from (0,0) we can see the building. So output -1.

    # However, consider two buildings: 
    # 1 1
    # 2 1
    # Then from (0,0): 
    #   For building 1: (1,1): the line from (0,0) to (1,1) is y=x. At x=1, y=1 -> touches the top. But if the condition is strict (must be above), then building 1 is not visible? Actually, the condition is that the line segment from (0,0) to (1,1) must not intersect any other building. There is building 2 at (2,1). The line segment from (0,0) to (1,1) does not reach building 2, so