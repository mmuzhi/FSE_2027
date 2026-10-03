import re
from typing import List
from collections import Counter

class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        paragraph = re.sub("[.,!?;']", ' ', paragraph.lower()).split()
        banned_set = set(banned)
        paragraph = list(filter(lambda x: x not in banned_set, paragraph))
        return Counter(paragraph).most_common(1)[0][0]