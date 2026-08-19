class AutomaticGuitarSimulator:
    def __init__(self, text):
        self.play_text = text

    def interpret(self, display=False):
        if self.play_text is None or not self.play_text.strip():
            return None

        play_list = []
        play_segs = self.play_text.split(" ")
        for play_seg in play_segs:
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
            play_list.append(self.ChordTune(play_chord, play_value))
            if display:
                self.display(play_chord, play_value)
        return play_list

    def display(self, key, value):
        return "Normal Guitar Playing -- Chord: {}, Play Tune: {}".format(key, value)

    class ChordTune:
        def __init__(self, chord, tune):
            self._chord = chord
            self._tune = tune

        @property
        def chord(self):
            return self._chord

        @property
        def tune(self):
            return self._tune

        def get_chord(self):
            return self._chord

        def get_tune(self):
            return self._tune

        def __eq__(self, other):
            if self is other:
                return True
            if type(other) is not AutomaticGuitarSimulator.ChordTune:
                return False
            return self._chord == other._chord and self._tune == other._tune

        def __hash__(self):
            return hash((self._chord, self._tune))