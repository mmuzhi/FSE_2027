import random


class MusicPlayer:
    def __init__(self):
        # C++ seeds std::rand here, but it is never used afterwards;
        # Python's random module seeds itself, so no extra action needed.
        self.playlist = []
        self.current_song = ""
        self.volume = 50

    def add_song(self, song):
        self.playlist.append(song)

    def remove_song(self, song):
        if song in self.playlist:
            self.playlist.remove(song)  # removes first occurrence, like std::find + erase
            if self.current_song == song:
                self.stop()

    def play(self):
        if self.playlist:
            if self.current_song:
                if self.current_song in self.playlist:
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
                return False  # it == end()
            if idx + 1 < len(self.playlist):  # (it + 1) != end()
                self.current_song = self.playlist[idx + 1]
                return True
            return False
        return False

    def previous_song(self):
        if self.current_song:
            try:
                idx = self.playlist.index(self.current_song)
            except ValueError:
                idx = len(self.playlist)  # it == end()
            if idx != 0:  # it != begin()
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