class Solution:
    def maxSubstringLength(self, s: str, k: int) -> bool:
        n = len(s)
        if k == 0:
            return True
        
        # Precompute left and right sets for each index
        left_set = [set() for _ in range(n)]
        right_set = [set() for _ in range(n)]
        
        # left_set[i] contains characters from 0 to i-1
        for i in range(1, n):
            left_set[i] = left_set[i-1].union({s[i-1]})
        
        # right_set[i] contains characters from i+1 to n-1
        for i in range(n-2, -1, -1):
            right_set[i] = right_set[i+1].union({s[i+1]})
        
        # Now, we want to find all special substrings (each is a contiguous substring that satisfies the condition)
        # But note: the condition for substring from i to j is that for every char in s[i:j+1], char is not in left_set[i] and not in right_set[j].
        # However, we are only interested in the maximum number of disjoint special substrings.
        
        # But note: the condition is independent of other substrings. So, we can consider each special substring individually.
        # But the problem is: we need to select disjoint ones. So, we can use a greedy approach: find the longest special substring and then remove it and then find the next, etc. But that might not be optimal.

        # Alternatively, we can note that each special substring must be contained in a part of the string where the set of characters in the substring does not appear elsewhere. 

        # But note: the condition is global. 

        # Another observation: a special substring must be such that it is contained in a maximal block where the characters in the substring are unique to that block. 

        # But actually, the condition is: the substring must not contain any character that appears outside. 

        # We can try to find all maximal special substrings. 

        # However, note that the problem constraints: n up to 50,000 and k up to 26. 

        # We can use a two-pointer method to find all special substrings? But that would be O(n^2) which is too slow.

        # We need to find a better way.

        # Let me think: 

        # A substring is special if the set of characters in it does not intersect with the left_set[i] and right_set[j] (for substring from i to j). 

        # But note, the condition is: for each char in the substring, it must not be in left_set[i] and not in right_set[j]. 

        # This is equivalent to: the set of characters in the substring is disjoint from left_set[i] and right_set[j]. 

        # Now, note that the entire string is fixed. 

        # We can precompute for each index i, the set of characters that are "available" to the left and right.

        # But then, how to count the maximum number of disjoint special substrings?

        # We can use a greedy algorithm: 

        # 1. Find all candidate special substrings (each contiguous substring that satisfies the condition). 
        # 2. Then, use interval scheduling (by sorting by end index) to select as many as possible.

        # But step 1 is too expensive.

        # Another idea: 

        # Note that each special substring must be contained in a part of the string that is "isolated" by the characters. 

        # Actually, consider: if a character appears only once in the entire string, then any substring containing that character and not containing any other character that appears outside is a candidate. 

        # But wait, the condition is that the substring must not contain any character that appears outside. 

        # So, for a substring to be special, it must not contain any character that appears outside. 

        # This means that the substring must be contained in a part of the string that is "closed" for all characters it contains. 

        # But note, the entire string might have multiple occurrences of a character. 

        # We can try to find all maximal substrings that are "closed" for their characters. 

        # Actually, a special substring is a contiguous substring that is a "maximal" substring in the sense that if we extend it, then the condition breaks. 

        # But note, the condition is not about maximality, but about the uniqueness of characters.

        # Alternatively, we can consider: 

        # For each index i, we can try to extend to the right as long as the condition holds. 

        # But the condition is global. 

        # However, we can use the following: 

        # Let's define a