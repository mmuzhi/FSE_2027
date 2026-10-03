class AutomaticGuitarSimulator:
    def __init__(self, text: str = None):
        self.playText = text

    def interpret(self, display: bool = False):
        if self.playText is None or self.playText.strip() == '':
            return None

        play_list = []
        play_segs = self.playText.split(' ')
        for play_seg in play_segs:
            if play_seg.strip() == '':
                continue
            pos = 0
            for ch in play_seg:
                if ch.isalpha():
                    pos += 1
                else:
                    break
            play_chord = play_seg[:pos]
            play_value = play_seg[pos:]
            play_list.append(ChordTune(play_chord, play_value))
            if display:
                self.display(play_chord, play_value)
        return play_list

    def display(self, key: str, value: str) -> str:
        return f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}"

    class ChordTune:
        def __init__(self, chord: str, tune: str):
            self.chord = chord
            self.tune = tune

        def getChord(self) -> str:
            return self.chord

        def getTune(self) -> str:
            return self.tune

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or not isinstance(other, AutomaticGuitarSimulator.ChordTune):
                return False
            return self.chord == other.chord and self.tune == other.tune

        def __hash__(self):
            return hash((self.chord, self.tune))