from collections import namedtuple

# Define PlayItem using namedtuple
PlayItem = namedtuple('PlayItem', ['Chord', 'Tune'])

class AutomaticGuitarSimulator:
    def __init__(self, text):
        self.play_text = text

    def interpret(self, display=False):
        if not self.play_text:
            return []

        play_list = []
        tokens = self.play_text.split()
        
        for token in tokens:
            # Find the position where non-alphabetic characters start
            i = 0
            while i < len(token) and token[i].isalpha():
                i += 1
            
            chord = token[:i]
            tune = token[i:]
            
            item = PlayItem(Chord=chord, Tune=tune)
            play_list.append(item)
            
            if display:
                print(self.format_display(chord, tune))
                
        return play_list

    def format_display(self, key, value):
        return f"Normal Guitar Playing -- Chord: {key}, Play Tune: {value}"