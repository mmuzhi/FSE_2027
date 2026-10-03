import sys

def main():
    data = sys.stdin.read().splitlines()
    q = int(data[0])
    total_wait = 0
    # We'll maintain a list (or other structure) of the "planted base" for each plant.
    # But we cannot store all plants and update their heights for each harvest because Q can be 200000 and harvest queries can be many.

    # Instead, we can use a Fenwick tree or segment tree? But note: the condition is "harvest all plants with height >= H", and the height of a plant is (total_wait - base_plant) where base_plant is the total_wait at the time of planting.

    # Actually, let's define:
    #   Let base_plant[i] = the total_wait accumulated just before the plant was added (so the plant's height is total_wait - base_plant[i]).
    #   Then the condition for harvesting is: total_wait - base_plant[i] >= H  => base_plant[i] <= total_wait - H.

    # So we need to count the number of plants that were planted with base_plant[i] <= (total_wait - H).

    # But note: the plants are added one by one, and the base_plant for a plant is the total_wait at the moment of planting.

    # We can use a Fenwick tree (Binary Indexed Tree) or a segment tree to count the number of plants that were planted with base_plant <= X.

    # Steps:
    #   Let events = []
    #   We'll record:
    #       For type 1: record the current total_wait as the base_plant for that plant.
    #       For type 2: update total_wait by adding T.
    #       For type 3: we want to count the plants that have base_plant <= (total_wait - H). But note: if total_wait - H is negative, then no plant qualifies.

    # However, we must note: the base_plant for a plant is the total_wait at the time of planting, and then the plant's height is total_wait (current) - base_plant.

    # We need to collect all the base_plant values and then for a query type 3, we want to count the plants with base_plant <= (total_wait - H).

    # But note: the base_plant values are increasing because total_wait is increasing (since T>=1). So we can use a Fenwick tree that is built on the base_plant values.

    # However, the base_plant values can be very large (up to 10^9 * 200000) but we don't know the range in advance.

    # Alternatively, we can use a balanced BST or a sorted list and use bisect. But we need to update and query the count.

    # We can use a Fenwick tree with coordinate compression.

    # Steps for Fenwick tree:
    #   We will collect all base_plant values (from type 1 queries) and also the thresholds (total_wait - H) for type 3 queries.
    #   Then compress the coordinates.

    # But note: the base_plant values are the total_wait at the time of planting, and total_wait is updated by type 2 queries. The base_plant for a plant is the total_wait just before the type 1 query.

    # We can do:
    #   Let events = []
    #   Let base_plant_list = []
    #   Let total_wait = 0
    #   Let queries = []
    #   For i in range(1, q+1):
    #       if data[i] == '1':
    #           base_plant_list.append(total_wait)
    #           queries.append(('1', total_wait))
    #       elif data[i].startswith('2'):
    #           T = int(data[i].split()[1])
    #           total_wait += T
    #           queries.append(('2', T))
    #       elif data[i].startswith('3'):
    #           H = int(data[i].split()[1])
    #           queries.append(('3', H))

    #   Then we need to collect all base_plant values and all (total_wait - H) for type 3 queries. But note: the total_wait at the time of type 3 query is the current total_wait (which is the sum of all previous wait queries). However, the base_plant values are from the past.

    #   Actually, we can compress the coordinates of all base_plant values and all thresholds (which are total_wait - H) from type 3 queries.

    #   But note: the base_plant values are the total_wait at the time of planting, and the thresholds are (current total_wait - H). The current total_wait is the sum of all wait queries up