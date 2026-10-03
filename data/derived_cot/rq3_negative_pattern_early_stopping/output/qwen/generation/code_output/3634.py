class Solution:
    def calculateScore(self, s: str) -> int:
        n = len(s)
        # Create a mapping from each character to its mirror
        mirror_map = {}
        for i, char in enumerate("abcdefghijklmnopqrstuvwxyz"):
            mirror_char = "zyxwvutsrqponmlkjihgfedcb"[i]
            mirror_map[char] = mirror_char
            mirror_map[mirror_char] = char
        
        # We'll maintain a dictionary for each character: a sorted list of indices that are unmarked and have been seen (but not necessarily used)
        # But we need to update these lists as we mark indices.
        # Alternatively, we can use a dictionary that maps character to a list of indices (and then use a pointer to the next available index?).
        # But we need to quickly find the largest index less than i for a given character.

        # Instead, we can use a dictionary that maps character to a sorted list of indices (initially all indices for that character) and then remove as we mark.
        # But we have to consider that the same character can appear multiple times.

        # Alternatively, we can precompute the positions for each character and then use a pointer for each character to the next available (largest) index less than i.
        # But we need to update the available indices.

        # Let's use a dictionary that maps character to a sorted list of indices (initially all indices where the character appears). Then, for each i, we look at the mirror character, and then in the sorted list for that mirror character, we find the largest index less than i. Then, if found, we remove that index from the list and add the score.

        # But we have to consider that the same index might be used for multiple pairs? No, because once marked, it's removed.

        # Steps:
        # 1. Precompute mirror_map for all lowercase letters.
        # 2. For each character, create a sorted list of indices where it appears in s.
        # 3. Also, we need to keep track of which indices are marked. But we can use the fact that we are removing from the lists.

        # However, we cannot precompute the sorted list for each character and then remove from it because the removal might be arbitrary and the list is sorted.

        # We can use a dictionary that maps character to a sorted list, and then use bisect to find the insertion point and then remove the element. But removal from a sorted list is O(n). 

        # Alternatively, we can use a balanced BST simulation with a sorted list and use the "bisect" module to find the element and then remove it. But removal is still O(n) per operation.

        # But note: the total number of removals is at most n (each index is removed once). So worst-case, we do n removals, each O(n), so O(n^2). With n=10^5, that's 10^10 operations, which is too slow in Python.

        # We need a more efficient data structure.

        # Another idea: use a pointer for each character that points to the next available index (from the rightmost). But we need to store the indices in a way that we can quickly find the largest index less than i.

        # Alternatively, we can use a Fenwick tree or segment tree to mark indices and then query for the maximum index less than i that is unmarked and has the mirror character. But that might be too complex.

        # Let me think differently: we are iterating from left to right. For each index i, we want to find the closest unmarked j (j < i) such that s[j] is the mirror of s[i]. 

        # We can maintain an array `marked` of booleans, but that doesn't help with finding the closest j.

        # Alternatively, we can use a stack. But the condition is about the mirror, not about adjacent characters.

        # Another idea: precompute for each index i, the mirror character. Then, for each index i, we want to find the closest j (to the left) that is unmarked and has the mirror character. 

        # We can store, for each character, a list of indices (in increasing order) that are unmarked. Then, for a given i, for the mirror character, we can do a binary search to find the largest index less than i in that list. Then, if found, we remove that index from the list and add the score.

        # But the removal from the list is O(n) per removal. However, the total number of removals is at most n (each index is removed once). So worst-case, the total operations would be O(n^2). 

        # But n can be 10^5, so worst-case 10^10 operations, which is too slow in Python