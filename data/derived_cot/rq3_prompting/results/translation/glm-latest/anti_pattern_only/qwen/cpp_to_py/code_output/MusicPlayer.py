import random
import time


class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.current_song = ""
        self.volume = 50
        random.seed(int(time.time()))

    def add_song(self, song):
        self.playlist.append(song)

    def remove_song(self, song):
        if song in self.playlist:
            self.playlist.remove(song)  # removes first occurrence
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
            if self.current_song in self.playlist:
                i = self.playlist.index(self.current_song)
                if i + 1 < len(self.playlist):
                    self.current_song = self.playlist[i + 1]
                    return True
            return False
        return False

    def previous_song(self):
        if not self.current_song:
            return False
        if self.current_song in self.playlist:
            i = self.playlist.index(self.current_song)
            if i > 0:
                self.current_song = self.playlist[i - 1]
                return True
            return False
        # Not found: find() returns end().
        if self.playlist:
            # end() != begin() when the playlist is non-empty,
            # so *(it - 1) is the last element (quirky C++ behavior kept).
            self.current_song = self.playlist[-1]
            return True
        return False

    def set_volume(self, volume):
        if self._is_valid_volume(volume):
            self.volume = volume
            return True
        return False

    def shuffle(self):
        if self.playlist:
            # Fresh non-deterministic generator, mirroring
            # std::random_device-seeded std::mt19937 per call.
            rng = random.Random()
            rng.shuffle(self.playlist)
            return True
        return False

    def _is_valid_volume(self, volume):
        return 0 <= volume <= 100