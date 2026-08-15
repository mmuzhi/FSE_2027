import re
from typing import List
from collections import Counter

class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        banned_set = {b.lower() for b in banned}
        words = [
            word for word in re.sub(r"[.,!?;']", ' ', paragraph.lower()).split()
            if word not in banned_set
        ]
        return Counter(words).most_common(1)[0][0]