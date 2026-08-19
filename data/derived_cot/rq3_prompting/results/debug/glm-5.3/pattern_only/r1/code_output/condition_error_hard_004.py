import collections


class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        indexes = collections.defaultdict(collections.deque)
        for index, character in enumerate(s):
            indexes[int(character)].append(index)

        for character in t:
            character_designation = int(character)
            if character_designation not in indexes or not indexes[character_designation]:
                return False
            for lesser_character in range(character_designation):
                if indexes[lesser_character] and indexes[lesser_character][0] < indexes[character_designation][0]:
                    return False
            indexes[character_designation].popleft()
            if not indexes[character_designation]:
                indexes.pop(character_designation)

        # if all characters were able to be matched in order, succeed
        return True