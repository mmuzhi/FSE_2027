import random
import time


class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current_song = ""
        self.volume = 50
        random.seed(time.time())

    def add_song(self, song):
        self.playlist.append(song)

    def remove_song(self, song):
        if song in self.playlist:
            self.playlist.remove(song)
            if self.current_song == song:
                self.stop()

    def play(self):
        if self.playlist:
            if self.current_song:
                for x in self.playlist:
                    if x == self.current_song:
                        return self.current_song
                return self.playlist[0]
            else:
                return self.playlist[0]
        return ""

    def stop(self):
        if self.current_song:
            self.current_song = ""
            return True
        return False

    def switch_song(self):
        if self.current_song:
            try:
                idx = self.playlist.index(self.current_song)
            except ValueError:
                return False
            if idx + 1 < len(self.playlist):
                self.current_song = self.playlist[idx + 1]
                return True
            return False
        return False

    def previous_song(self):
        if self.current_song:
            try:
                idx = self.playlist.index(self.current_song)
            except ValueError:
                # C++ std::find returns end() when not found; end() != begin()
                # for a non-empty list, so *(it - 1) yields the last element.
                idx = len(self.playlist)
            if idx != 0:
                self.current_song = self.playlist[idx - 1]
                return True
        return False

    def set_volume(self, volume):
        if self._is_valid_volume(volume):
            self.volume = volume
            return True
        return False

    def shuffle(self):
        if self.playlist:
            random.shuffle(self.playlist)
            return True
        return False

    def _is_valid_volume(self, volume):
        return 0 <= volume <= 100