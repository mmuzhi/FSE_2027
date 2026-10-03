class Solution:
    def findAnswer(self, parent: List[int], s: str) -> List[bool]:
        n = len(parent)
        children = [[] for _ in range(n)]
        for i in range(1, n):
            children[parent[i]].append(i)
        for i in range(n):
            children[i].sort()

        # We'll do a DFS to compute the DFS string for each node, but we cannot store the entire string.
        # Instead, we can store the entire string for the root? But that's too long.

        # Alternatively, we can use a two-pass method: one to compute the entire DFS string for the root, but then how to check for each node?

        # Actually, note: the DFS string for node i is the entire traversal of the subtree rooted at i. And the problem requires checking for each node i independently.

        # We can do a DFS from the root and for each node, we can compute the entire DFS string for the subtree, but that would be O(n^2) in the worst case.

        # But n can be 10^5, so we need an efficient method.

        # Another idea: use a hashing method to compute the entire string for the root, but then how to check for each node?

        # Alternatively, we can use a stack-based approach or iterative DFS to build the string for the root, but then how to extract the substring for each node?

        # Let me re-read the problem: for each node i, we empty the string and call dfs(i). So we need to compute the DFS string for each node independently.

        # But note: the DFS string for node i is the DFS of its subtree. The DFS of the subtree rooted at i is built by visiting children in increasing order and then appending s[i].

        # We can precompute the DFS order (the order of nodes visited) for the entire tree, but that doesn't directly help.

        # Another idea: use a technique similar to "String Hashing" to check for palindrome in the entire string without building it.

        # But the entire string for node i is the concatenation of the DFS strings of its children (each child's DFS string is the DFS of its subtree) and then s[i].

        # The entire string for node i is the DFS traversal of the subtree. The DFS traversal order is: first the children's DFS (in increasing order) and then the node's character.

        # The entire string for node i is fixed. But we cannot build it for each node.

        # We need to find a way to compute the entire string for node i without building it.

        # Observation: The DFS string for node i is the concatenation of the DFS strings of its children (in increasing order) and then s[i]. 

        # But the DFS string for a child is the DFS string of its subtree. 

        # We can precompute the entire DFS string for the root, but then how to get the DFS string for a node i? 

        # Actually, the DFS string for node i is a substring of the root's DFS string? Not exactly, because the root's DFS string includes the entire tree, but the DFS string for node i is only the part from node i's subtree.

        # But the root's DFS string is built by starting at root and then visiting children in increasing order. The DFS string for node i is built by starting at i and then visiting its children in increasing order. 

        # The two are different: the root's DFS string includes the entire tree, while the DFS string for node i is only the subtree of i.

        # So we need to compute for each node independently.

        # But note: the DFS string for node i is the DFS of its subtree. The DFS of the subtree rooted at i is independent of the rest of the tree.

        # We can do a DFS from node i and build the string, but that would be O(n) per node, leading to O(n^2) overall.

        # We need a better approach.

        # Let me consider the following: 

        # The DFS string for node i is: 
        #   T(i) = (T(child1)) + (T(child2)) + ... + (T(childk)) + s[i]

        # We can store for each node the entire DFS string as a linked list or use a rolling hash to compute the hash of T(i) without storing the entire string.

        # But then, to check if T(i) is a palindrome, we need the hash of T(i) and the hash of the reversed T(i). 

        # However, the reversed T(i) is not simply the reversed order of the DFS because the DFS is depth-first and the children are visited in increasing order. The entire string T(i) is the concatenation of the DFS strings of the children (each child's DFS string is the DFS of its subtree) and then s