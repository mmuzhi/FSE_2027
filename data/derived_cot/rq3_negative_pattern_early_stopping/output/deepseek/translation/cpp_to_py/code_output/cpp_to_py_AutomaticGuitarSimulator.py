class PlayItem:
    def __init__(self, chord: str, tune: str):
        self.Chord = chord
        self.Tune = tune

class AutomaticGuitarSimulator:
    def __init__(self, text: str):
        self.play_text = text

    def interpret(self, display: bool = False):
        play_list = []
        if not self.play_text:
            return play_list

        tokens = self.play_text.split()
        for play_seg in tokens:
            pos = 0
            while pos < len(play_seg) and play_seg[pos].isalpha():
                pos += 1

            play_chord = play_seg[:pos]
            play_value = play_seg[pos:]

            item = PlayItem(play_chord, play_value)
            play_list.append(item)

            if display:
                print(self.format_display(play_chord, play_value))

        return play_list

    def format_display(self, key: str, value: str) -> str:
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value