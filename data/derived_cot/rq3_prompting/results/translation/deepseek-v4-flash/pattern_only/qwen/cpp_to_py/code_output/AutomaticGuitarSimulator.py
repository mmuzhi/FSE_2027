from dataclasses import dataclass
from typing import List


@dataclass
class PlayItem:
    Chord: str
    Tune: str


class AutomaticGuitarSimulator:
    def __init__(self, text: str):
        self.play_text = text

    def interpret(self, display: bool = False) -> List[PlayItem]:
        play_list: List[PlayItem] = []
        if not self.play_text:
            return play_list

        for play_seg in self.play_text.split():
            pos = 0
            while pos < len(play_seg) and self._is_alpha(play_seg[pos]):
                pos += 1

            play_chord = play_seg[:pos]
            play_value = play_seg[pos:]

            play_list.append(PlayItem(play_chord, play_value))

            if display:
                print(self.format_display(play_chord, play_value), flush=True)

        return play_list

    def format_display(self, key: str, value: str) -> str:
        return f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}"

    @staticmethod
    def _is_alpha(c: str) -> bool:
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z')