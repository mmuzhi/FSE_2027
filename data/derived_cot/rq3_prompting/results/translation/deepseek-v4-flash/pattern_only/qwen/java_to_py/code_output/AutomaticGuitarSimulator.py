class AutomaticGuitarSimulator:
    class ChordTune:
        def __init__(self, chord, tune):
            self.chord = chord
            self.tune = tune

        def getChord(self):
            return self.chord

        def getTune(self):
            return self.tune

        def __eq__(self, other):
            if self is other:
                return True
            if other is None or type(self) is not type(other):
                return False
            return self.chord == other.chord and self.tune == other.tune

        def __hash__(self):
            return hash((self.chord, self.tune))

    def __init__(self, text):
        self.playText = text

    def interpret(self, display):
        if self.playText is None or _java_trim(self.playText) == "":
            return None

        playList = []
        playSegs = self.playText.split(" ")
        for playSeg in playSegs:
            if _java_trim(playSeg) == "":
                continue
            pos = 0
            for ele in playSeg:
                if ele.isalpha():
                    pos += 1
                else:
                    break
            playChord = playSeg[:pos]
            playValue = playSeg[pos:]
            playList.append(AutomaticGuitarSimulator.ChordTune(playChord, playValue))
            if display:
                self.display(playChord, playValue)
        return playList

    def display(self, key, value):
        return "Normal Guitar Playing -- Chord: %s, Play Tune: %s" % (key, value)


def _java_trim(s):
    start = 0
    end = len(s)
    while start < end and s[start] <= ' ':
        start += 1
    while end > start and s[end - 1] <= ' ':
        end -= 1
    return s[start:end]