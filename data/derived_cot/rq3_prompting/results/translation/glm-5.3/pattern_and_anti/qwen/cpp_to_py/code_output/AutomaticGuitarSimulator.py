class PlayItem:
    def __init__(self, chord, tune):
        self.Chord = chord
        self.Tune = tune


class AutomaticGuitarSimulator:
    def __init__(self, text):
        self.play_text = text

    def interpret(self, display=False):
        play_list = []
        if not self.play_text:
            return play_list

        for play_seg in self.play_text.split():
            pos = 0
            while pos < len(play_seg) and (
                ('a' <= play_seg[pos] <= 'z') or ('A' <= play_seg[pos] <= 'Z')
            ):
                pos += 1

            play_chord = play_seg[:pos]
            play_value = play_seg[pos:]

            item = PlayItem(play_chord, play_value)
            play_list.append(item)

            if display:
                print(self.format_display(play_chord, play_value))

        return play_list

    def format_display(self, key, value):
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value