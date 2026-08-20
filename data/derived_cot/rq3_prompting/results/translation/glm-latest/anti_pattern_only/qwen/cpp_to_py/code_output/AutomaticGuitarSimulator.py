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
            while pos < len(play_seg) and play_seg[pos].isalpha():
                pos += 1

            play_chord = play_seg[:pos]
            play_value = play_seg[pos:]

            play_list.append(PlayItem(play_chord, play_value))

            if display:
                print(self.format_display(play_chord, play_value))

        return play_list

    def format_display(self, key: str, value: str) -> str:
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value