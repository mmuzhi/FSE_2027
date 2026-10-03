class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        # Precompute the trie structure for all words
        trie = {}
        for word in words:
            node = trie
            for char in word:
                if char not in node:
                    node[char] = {}
                node = node[char]
        
        # Function to get the common prefix length for a given set of words (represented by indices)
        # But we cannot iterate over all combinations because n can be up to 10^5 and k up to 10^5, so that's too slow.
        # Instead, we need to use the trie and frequency counts.

        # We'll use a frequency array for each node in the trie, but we need to account for removals.

        # Alternatively, we can precompute a frequency array for each node, but then for each removal, we need to update the frequencies and then check for the longest common prefix.

        # However, the problem requires for each index i, remove words[i] and then find the answer.

        # Another idea: Instead of removing each word one by one, we can precompute the frequency of each word and then for each word, we can consider the set of words that are present at least k times (but not necessarily, because the common prefix might come from a set that doesn't have the same word repeated, but different words that share a long prefix).

        # Actually, the common prefix of a set of k strings is determined by the trie. The length is the depth at which the trie branches beyond k (i.e., the node at depth d has a frequency >= k, then the common prefix is at least d+1? Actually, no: the common prefix is the entire path until the node where the count drops below k? Not exactly.

        # Let me think: The common prefix of a set of strings is the longest string that is a prefix of all. In the trie, we can traverse until we find a node where the frequency (count of words passing through) is less than k. But wait, the frequency in the trie node is the count of words that have this prefix. But we are selecting k distinct words. So, for a node at depth d, if the frequency is >= k, then there are at least k words that have this prefix. But that doesn't necessarily mean that we can form a set of k words that have a common prefix of length d. Actually, it does: if the node at depth d has frequency >= k, then we can choose k words that all have the prefix up to d. But then, the common prefix of those k words is at least d. However, we want the maximum common prefix. So, we need to find the maximum d such that the node at depth d has frequency >= k.

        # But note: the common prefix of a set of k words must be a prefix that is common to all k. So, if we have a node at depth d with frequency >= k, then we can form a set of k words that share the prefix of length d. But the common prefix might be longer if the k words share more? Actually, no: the common prefix is the entire path until the point where they diverge. But if we are just counting the frequency of the prefix, then the maximum d for which the node has frequency >= k is the length of the common prefix for some set of k words.

        # However, consider: we might have two different sets of k words that have different common prefixes. We want the maximum common prefix length over all sets.

        # Actually, the maximum common prefix length is the maximum d such that there exists a set of k words that all have the prefix of length d. And that is equivalent to: the node at depth d has frequency >= k.

        # But wait, that is not entirely true. The frequency of the node at depth d is the count of words that have the prefix of length d. But if we have k words, they must all have the prefix of length d. So, if the node at depth d has frequency >= k, then we can choose k words that have that prefix. But the common prefix of those k words might be longer than d? Actually, no: the common prefix is exactly the path from the root to the node at depth d, because beyond d, the node branches. But if the node at depth d has frequency >= k, then we can form a set of k words that have the prefix of length d. But the common prefix of that set might be longer if the k words actually share more? Actually, no: the common prefix is the entire path until the point where they start to differ. But if we are just looking for the existence of a set of k words that have a common prefix of length d,