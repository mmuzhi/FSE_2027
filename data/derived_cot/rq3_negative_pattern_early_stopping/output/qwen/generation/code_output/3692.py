class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        m = len(p)
        # Find the positions of the two '*' in p
        stars = [i for i, char in enumerate(p) if char == '*']
        if len(stars) != 2:
            # According to the problem, there are exactly two, but just in case
            return -1
        
        # The three parts of the pattern
        part1 = p[:stars[0]]
        part2 = p[stars[0]+1:stars[1]]
        part3 = p[stars[1]+1:]
        
        # We'll use two pointers to find the minimal substring
        # The idea: for each starting index in s, we try to match part1, then part2, then part3, with the two stars matching any characters in between.
        # But that might be O(n^2). We need an efficient way.
        
        # Alternatively, we can use a two-pointer approach to find the minimal window that contains part1, part2, part3 in order, with the stars matching any characters.
        # But the stars can match any characters, so the window must contain part1, then part2, then part3, but the order is fixed and the parts must appear in order, but the stars can match any characters in between.
        
        # We can precompute the next occurrence of part1, then part2, then part3, but that might be complex.
        
        # Another idea: since the pattern has two stars, the minimal matching substring must start with part1 and end with part3. The part2 must appear in between. But the part2 might not be contiguous? Actually, no: the pattern is matched sequentially. So, the substring must have part1, then (any characters) then part2, then (any characters) then part3.
        
        # We can try to find all occurrences of part1 and part3, and then check if part2 is contained in between. But that might be too slow.
        
        # Alternatively, we can use a sliding window approach. We'll consider each starting index and then expand until we have a substring that matches the pattern. But that would be O(n^2) in worst-case, which is not acceptable for n=10^5.
        
        # We need a more efficient method.
        
        # Let me think: the pattern has two fixed parts (part1 and part3) and one variable part (part2). The minimal substring must start with part1 and end with part3. So, we can consider all starting positions where part1 occurs, and then for each starting position, we can find the minimal ending position where part3 occurs, and then check if part2 is contained in between (in order). But the part2 must appear in order and contiguously? Actually, no: the part2 is the substring between the two stars, so it must appear as a contiguous substring in the matching substring. Wait, no: the part2 is the substring between the two stars in the pattern. So, in the matching substring, after part1, we can have any characters, then part2 must appear (contiguously) and then any characters, then part3. So, part2 must appear as a contiguous substring in the matching substring, but not necessarily adjacent to part1 or part3.
        
        # Actually, the pattern is: [part1][*][part2][*][part3]. So, the matching substring must have part1, then any characters (which can include part2 and part3? No, because the pattern is matched in order. So, the order is: part1, then (any characters), then part2, then (any characters), then part3. So, part2 must appear after part1 and before part3, and part2 must be contiguous. Similarly, part1 and part3 must be contiguous? No, they can be separated by any characters (the stars). But part1 and part3 must appear in order, and part2 must appear between them (contiguously). So, the matching substring must have part1, then any characters (which can include part2 and part3? No, because part3 must come after part2). Actually, the order is fixed: part1, then (any characters) then part2, then (any characters) then part3. So, part2 must appear after part1 and before part3, and part2 must be contiguous. But part1 and part3 can be separated by any characters, including part2 and other characters.
        
        # Actually, the matching substring must have the following structure:
        #   [part1][any characters][part2][any characters][part3]
        # So, part2 must appear as a contiguous substring somewhere between part1 and part3.