import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    B = list(map(int, data[1+n:1+n+n-1]))
    boxes = B + [0]  # adding a zero to make it n boxes for simplicity, but we'll handle separately

    # Sort the toys and boxes
    A.sort()
    boxes.sort()

    # We are going to use a greedy approach: we need to cover the largest toys with the largest boxes.
    # The idea is to assign the smallest available box that can hold the toy, but we are allowed to use the new box (x) for any toy.

    # However, note that we have n-1 existing boxes and one new box. We need to assign each toy to a box.

    # Let's think: we can use the existing boxes for as many toys as possible, and the new box for the rest.

    # But the problem is: we don't know which toy goes to which box. We need to find the minimal x such that we can assign all.

    # Alternatively, we can think: what is the minimal x required? We must cover the largest toy that is not covered by the existing boxes.

    # Steps:
    # 1. Sort the toys (A) in increasing order.
    # 2. Sort the existing boxes (B) in increasing order.

    # We can try to assign the largest toys to the largest boxes (existing and new). But note: the new box is the largest (x) and we are trying to minimize x.

    # Another idea: we can use the existing boxes to cover as many of the smallest toys as possible. Then the remaining toys must be covered by the new box (and possibly some existing boxes if they are large enough).

    # But note: the new box is one box. So we can only use one box (the new one) for multiple toys? No, each box can contain one toy.

    # Actually, we have n boxes (n-1 existing and one new). Each toy must be in a separate box.

    # We can model this as: we have n boxes (the existing ones and the new one). We need to assign each toy to a box such that the box size >= toy size. We want the minimal x (the new box size) such that there exists an assignment.

    # This is similar to a matching problem: we have n boxes (with one box being x) and n toys. We need to match each toy to a box with box size >= toy size.

    # We can use a greedy matching: sort the toys and the boxes (including the new box) and then try to assign the smallest box that can hold the toy.

    # But we don't know x. We need to find the minimal x such that when we have the existing boxes and the new box (x), we can assign all toys.

    # We can do a binary search on x. The range for x is from 0 to maybe max(A) (but actually, the new box must be at least as large as the largest toy that isn't covered by existing boxes). But note: the existing boxes might not cover the largest toy.

    # Steps for binary search:
    #   low = 0, high = max(A) (or maybe max(A) + max(B) but we can set high = max(A) because if x is max(A), then the new box is at least as big as the largest toy, so it can cover the largest toy. But wait, maybe we don't need to go beyond max(A) because the new box only needs to be as big as the largest toy that isn't covered by existing boxes. But if the existing boxes don't cover the largest toy, then x must be at least that largest toy.

    # However, note: we have n boxes. The existing boxes might cover multiple toys. The new box is one box, so it can only cover one toy. But wait, no: the new box is one box, so it can only hold one toy. The other toys must be held by the existing boxes.

    # Actually, we have n-1 existing boxes and one new box (total n boxes). So we need to assign n toys to n boxes.

    # The problem is: we need to cover all n toys. The existing boxes can cover up to n-1 toys. The new box covers one. But the existing boxes might not be sufficient to cover all but one toy.

    # Actually, the minimal x must be at least the maximum toy that is not covered by the existing boxes. But we don't know which toys are covered by existing boxes.

    # Alternate approach:

    # 1. Sort the toys in descending order.
    # 2. Sort the existing boxes in descending order.
    # 3