class AutomaticGuitarSimulator:

    def __init__(self, text):
        self.playText = text

    def interpret(self, display):
        if self.playText is None or not self.playText.strip():
            return None

        play_list = []
        for play_seg in self.playText.split(" "):
            if not play_seg.strip():
                continue
            pos = 0
            for ele in play_seg:
                if ele.isalpha():
                    pos += 1
                    continue
                break
            play_chord = play_seg[:pos]
            play_value = play_seg[pos:]
            play_list.append(AutomaticGuitarSimulator.ChordTune(play_chord, play_value))
            if display:
                self.display(play_chord, play_value)
        return play_list

    def display(self, key, value):
        return "Normal Guitar Playing -- Chord: {}, Play Tune: {}".format(key, value)

    class ChordTune:
        def __init__(self, chord, tune):
            self.chord = chord
            self.tune = tune

        def get_chord(self):
            return self.chord

        def get_tune(self):
            return self.tune

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) is not type(other):
                return False
            return self.chord == other.chord and self.tune == other.tune

        def __hash__(self):
            return hash((self.chord, self.tune))