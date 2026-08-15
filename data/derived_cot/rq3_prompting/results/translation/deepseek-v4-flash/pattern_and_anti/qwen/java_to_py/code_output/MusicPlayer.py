import random


class MusicPlayer:
    def __init__(self):
        self.playlist = []
        self.currentSong = None
        self.volume = 50

    def addSong(self, song):
        self.playlist.append(song)

    def removeSong(self, song):
        if song in self.playlist:
            self.playlist.remove(song)
            if self.currentSong is not None and self.currentSong == song:
                self.stop()

    def play(self):
        if not self.playlist:
            return None
        if self.currentSong is not None:
            for song in self.playlist:
                if song == self.currentSong:
                    return self.currentSong
        return self.playlist[0]

    def stop(self):
        if self.currentSong is not None:
            self.currentSong = None
            return True
        return False

    def switchSong(self):
        if self.currentSong is None:
            return False
        try:
            currentIndex = self.playlist.index(self.currentSong)
        except ValueError:
            currentIndex = -1
        if currentIndex < len(self.playlist) - 1:
            self.currentSong = self.playlist[currentIndex + 1]
            return True
        return False

    def previousSong(self):
        if self.currentSong is None:
            return False
        try:
            currentIndex = self.playlist.index(self.currentSong)
        except ValueError:
            currentIndex = -1
        if currentIndex > 0:
            self.currentSong = self.playlist[currentIndex - 1]
            return True
        return False

    def setVolume(self, volume):
        if 0 <= volume <= 100:
            self.volume = volume
            return True
        return False

    def shuffle(self):
        if not self.playlist:
            return False
        random.shuffle(self.playlist)
        return True

    def getPlaylist(self):
        return self.playlist

    def setPlaylist(self, playlist):
        self.playlist = playlist

    def getCurrentSong(self):
        return self.currentSong

    def setCurrentSong(self, currentSong):
        self.currentSong = currentSong

    def getVolume(self):
        return self.volume