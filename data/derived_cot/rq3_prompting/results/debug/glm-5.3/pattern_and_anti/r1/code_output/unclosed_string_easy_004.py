#Import RegEx
import re
from collections import Counter
from typing import List

class Solution:
    def mostCommonWord(self, paragraph: str, banned: List[str]) -> str:
        paragraph = re.sub(r"[.,!?;']", ' ', paragraph.lower()).split(' ')
        paragraph = list(filter(lambda x: x not in banned + [''], paragraph))
        return Counter(paragraph).most_common(1)[0][0]