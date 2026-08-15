import re
from collections import Counter
from typing import List

class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        words = re.sub(r"[^a-zA-Z]", " ", paragraph.lower()).split()
        banned_set = {b.lower() for b in banned}
        words = [w for w in words if w not in banned_set]
        return Counter(words).most_common(1)[0][0]