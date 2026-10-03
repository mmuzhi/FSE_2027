class AutomaticGuitarSimulator:
    def __init__(self, text):
        self.playText = text

    def interpret(self, display):
        if self.playText is None or self.playText.strip() == "":
            return None

        play_list = []
        segments = self.playText.split()
        for seg in segments:
            if seg.strip() == "":
                continue
            pos = 0
            for char in seg:
                if char.isalpha():
                    pos += 1
                else:
                    break
            chord = seg[:pos]
            tune = seg[pos:]
            play_list.append(ChordTune(chord, tune))
            if display:
                self.display(chord, tune)
        return play_list

    def display(self, key, value):
        return f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}"

    class ChordTune:
        def __init__(self, chord, tune):
            self.chord = chord
            self.tune = tune

        def __eq__(self, other):
            if not isinstance(other, AutomaticGuitarSimulator.ChordTune):
                return False
            return self.chord == other.chord and self.tune == other.tune

        def __hash__(self):
            return hash((self.chord, self.tune))

# Example usage:
# simulator = AutomaticGuitarSimulator("C3/4 D5 E7")
# result = simulator.interpret(True)