class PlayItem:
    def __init__(self, chord, tune):
        self.Chord = chord
        self.Tune = tune


class AutomaticGuitarSimulator:
    def __init__(self, text):
        self._play_text = text

    def interpret(self, display=False):
        play_list = []
        if not self._play_text:
            return play_list

        for play_seg in self._play_text.split():
            pos = 0
            while pos < len(play_seg) and _is_alpha(play_seg[pos]):
                pos += 1

            play_chord = play_seg[:pos]
            play_value = play_seg[pos:]

            item = PlayItem(play_chord, play_value)
            play_list.append(item)

            if display:
                print(self.format_display(play_chord, play_value), flush=True)

        return play_list

    def format_display(self, key, value):
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value


def _is_alpha(ch):
    return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')