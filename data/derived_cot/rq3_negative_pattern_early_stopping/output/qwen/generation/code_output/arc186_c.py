import sys
import math

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        n = int(data[index]); m = int(data[index+1]); index += 2
        boxes = []
        for i in range(n):
            v = int(data[index]); p = int(data[index+1]); index += 2
            boxes.append((v, p))
            
        # We are to compute the maximum net gain (total received - total spent) that Mr. Box can achieve, 
        # but Mr. Ball will choose the ball type to minimize that. However, note that Mr. Box can choose which box to use for a given type.
        # Actually, the problem is equivalent to: Mr. Box wants to assign boxes to types (each box can be assigned to at most one type) and then the net gain for a type is (number of balls stored) * 1 - (cost of boxes assigned to that type). 
        # But the number of balls stored for a type is the total capacity of the boxes assigned to that type. However, Mr. Ball can choose to stop giving a type at any time. But since Mr. Ball has infinite balls, the game can go on until Mr. Box decides to stop or until a box is full. But Mr. Box can always continue to accept as long as there is space in some box for the type that Mr. Ball chooses. 

        # Actually, the optimal strategy for Mr. Box is to use the boxes to store as many balls as possible (to get more yen) but the cost is the price of the boxes. 

        # However, Mr. Ball can choose the type. So, for Mr. Box, he must ensure that for every type, if he wants to store balls of that type, he must have bought boxes for that type. 

        # But note: Mr. Box can buy boxes for a type only when a ball of that type is given and he accepts. 

        # The key observation: The game is equivalent to Mr. Box buying a set of boxes (each box has a capacity and a price) and then the total received is the sum of the capacities of the boxes (because each box can store up to its capacity, and Mr. Ball will give balls until the box is full, and then Mr. Box can use another box for that type). 

        # However, Mr. Ball can choose the order of types. He will try to minimize the net gain. 

        # But note: Mr. Box can choose which box to use for a given type. 

        # Actually, the problem can be reduced to: Mr. Box wants to select a set of boxes (each box can be used for one type) such that the total capacity (which is the total number of balls that can be stored) minus the total cost is maximized. But wait, the total capacity is the sum of the capacities of the boxes, and the total cost is the sum of the prices. 

        # However, there are M types. Mr. Box must assign boxes to types. But he can assign multiple boxes to the same type. 

        # But note: the condition for a box is that all balls in it are of the same type. So, a box can only be used for one type. 

        # So, the problem becomes: We have N boxes (each with capacity V_i and price P_i). We can assign each box to at most one type. We have M types. We want to maximize the total capacity (sum of V_i for all boxes used) minus the total price (sum of P_i for all boxes used). 

        # But wait, is that correct? 

        # Actually, Mr. Box can use a box for one type only. And the total number of balls stored is the sum of the capacities of the boxes assigned to each type. 

        # However, Mr. Ball can choose the order. He will try to force Mr. Box to not get as much as possible. 

        # But note: Mr. Box can always accept a ball and put it in a box (if he has bought it) and get 1 yen. The only way to prevent getting 1 yen is to either not accept the ball (end the game) or to not have a box for that type (then the condition fails). 

        # However, Mr. Box can choose to buy boxes as needed. 

        # The optimal strategy for Mr. Box is to buy a set of boxes that maximizes (total capacity - total cost). Then, the net gain is (total capacity) - (total cost). 

        # But wait, is that the case? 

        # Consider: Mr. Box buys a set of boxes. Then, for each type, he can store up to the total capacity of the boxes assigned