import random
from typing import List, Optional


class MusicPlayer:
    def __init__(self):
        self._playlist: List[str] = []
        self._current_song: Optional[str] = None
        self._volume: int = 50

    def addSong(self, song: str) -> None:
        self._playlist.append(song)

    def removeSong(self, song: str) -> None:
        if song in self._playlist:
            self._playlist.remove(song)
            if self._current_song is not None and self._current_song == song:
                self.stop()

    def play(self) -> Optional[str]:
        if not self._playlist:
            return None
        if self._current_song is not None and self._current_song in self._playlist:
            return self._current_song
        return self._playlist[0]

    def stop(self) -> bool:
        if self._current_song is not None:
            self._current_song = None
            return True
        return False

    def switchSong(self) -> bool:
        if self._current_song is None:
            return False
        try:
            idx = self._playlist.index(self._current_song)
        except ValueError:
            idx = -1
        if idx < len(self._playlist) - 1:
            self._current_song = self._playlist[idx + 1]
            return True
        return False

    def previousSong(self) -> bool:
        if self._current_song is None:
            return False
        try:
            idx = self._playlist.index(self._current_song)
        except ValueError:
            idx = -1
        if idx > 0:
            self._current_song = self._playlist[idx - 1]
            return True
        return False

    def setVolume(self, volume: int) -> bool:
        if 0 <= volume <= 100:
            self._volume = volume
            return True
        return False

    def shuffle(self) -> bool:
        if not self._playlist:
            return False
        random.shuffle(self._playlist)
        return True

    def getPlaylist(self) -> List[str]:
        return self._playlist

    def setPlaylist(self, playlist: List[str]) -> None:
        self._playlist = playlist

    def getCurrentSong(self) -> Optional[str]:
        return self._current_song

    def setCurrentSong(self, currentSong: Optional[str]) -> None:
        self._current_song = currentSong

    def getVolume(self) -> int:
        return self._volume