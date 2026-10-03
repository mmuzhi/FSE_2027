class PlayItem:
    def __init__(self, Chord, Tune):
        self.Chord = Chord
        self.Tune = Tune


class AutomaticGuitarSimulator:
    def __init__(self, text):
        self.play_text = text

    def interpret(self, display=False):
        play_list = []
        if not self.play_text:
            return play_list

        play_segs = self.play_text.split()

        for play_seg in play_segs:
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

    def format_display(self, key, value):
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value