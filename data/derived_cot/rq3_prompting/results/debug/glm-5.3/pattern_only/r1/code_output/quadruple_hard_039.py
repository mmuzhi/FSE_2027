import random
from typing import List


class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        def size(node):
            return node[2] if node else 0

        def pull(node):
            node[2] = size(node[4]) + size(node[5]) + node[1]

        def rot_right(node):
            left = node[4]
            node[4] = left[5]
            left[5] = node
            pull(node)
            pull(left)
            return left

        def rot_left(node):
            right = node[5]
            node[5] = right[4]
            right[4] = node
            pull(node)
            pull(right)
            return right

        def insert(node, key):
            # node = [key, cnt, subtree_size, priority, left, right]
            if not node:
                return [key, 1, 1, random.random(), None, None]
            if key == node[0]:
                node[1] += 1
            elif key < node[0]:
                node[4] = insert(node[4], key)
                if node[4][3] > node[3]:
                    node = rot_right(node)
            else:
                node[5] = insert(node[5], key)
                if node[5][3] > node[3]:
                    node = rot_left(node)
            pull(node)
            return node

        def remove(node, key):
            if not node:
                return None
            if key == node[0]:
                if node[1] > 1:
                    node[1] -= 1
                else:
                    if not node[4] or not node[5]:
                        return node[4] or node[5]
                    if node[4][3] > node[5][3]:
                        node = rot_right(node)
                        node[5] = remove(node[5], key)
                    else:
                        node = rot_left(node)
                        node[4] = remove(node[4], key)
            elif key < node[0]:
                node[4] = remove(node[4], key)
            else:
                node[5] = remove(node[5], key)
            pull(node)
            return node

        def get(node, rank):
            # rank is 1-indexed: returns rank-th smallest key
            left_size = size(node[4])
            if rank <= left_size:
                return get(node[4], rank)
            if rank <= left_size + node[1]:
                return node[0]
            return get(node[5], rank - left_size - node[1])

        tree = None
        ans = []
        for i, x in enumerate(nums):
            tree = insert(tree, x)
            if size(tree) > k:
                tree = remove(tree, nums[i - k])
            if size(tree) == k:
                if k % 2 == 1:
                    ans.append(float(get(tree, k // 2 + 1)))
                else:
                    ans.append((get(tree, k // 2) + get(tree, k // 2 + 1)) / 2)
        return ans