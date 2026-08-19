#pragma once

#include <algorithm>
#include <optional>
#include <random>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

class MusicPlayer {
private:
    std::vector<std::string> playlist;
    std::optional<std::string> currentSong;  // Java null == std::nullopt
    int volume;

    // Java List.indexOf semantics: first index of value, or -1 if absent.
    int indexOf(const std::string& value) const {
        auto it = std::find(playlist.begin(), playlist.end(), value);
        return it == playlist.end() ? -1 : static_cast<int>(it - playlist.begin());
    }

public:
    MusicPlayer() : volume(50) {}

    void addSong(const std::string& song) {
        playlist.push_back(song);
    }

    void removeSong(const std::string& song) {
        auto it = std::find(playlist.begin(), playlist.end(), song);
        if (it != playlist.end()) {
            playlist.erase(it);  // Java List.remove(Object) removes first occurrence only
            if (currentSong.has_value() && *currentSong == song) {
                stop();
            }
        }
    }

    std::optional<std::string> play() {
        if (playlist.empty()) {
            return std::nullopt;
        }
        if (currentSong.has_value()) {
            for (const std::string& song : playlist) {
                if (song == *currentSong) {
                    return currentSong;
                }
            }
        }
        return playlist[0];
    }

    bool stop() {
        if (currentSong.has_value()) {
            currentSong.reset();
            return true;
        }
        return false;
    }

    bool switchSong() {
        if (!currentSong.has_value()) {
            return false;
        }
        int currentIndex = indexOf(*currentSong);
        // int math on purpose: preserves Java behavior when currentIndex == -1
        if (currentIndex < static_cast<int>(playlist.size()) - 1) {
            currentSong = playlist[static_cast<size_t>(currentIndex + 1)];
            return true;
        }
        return false;
    }

    bool previousSong() {
        if (!currentSong.has_value()) {
            return false;
        }
        int currentIndex = indexOf(*currentSong);
        if (currentIndex > 0) {
            currentSong = playlist[static_cast<size_t>(currentIndex - 1)];
            return true;
        }
        return false;
    }

    bool setVolume(int volume) {
        if (volume >= 0 && volume <= 100) {
            this->volume = volume;
            return true;
        }
        return false;
    }

    bool shuffle() {
        if (playlist.empty()) {
            return false;
        }
        std::mt19937 rng(std::random_device{}());
        std::shuffle(playlist.begin(), playlist.end(), rng);
        return true;
    }

    // Java returns the live list reference; expose a mutable reference.
    std::vector<std::string>& getPlaylist() {
        return playlist;
    }

    void setPlaylist(std::vector<std::string> playlist) {
        this->playlist = std::move(playlist);
    }

    const std::optional<std::string>& getCurrentSong() const {
        return currentSong;
    }

    void setCurrentSong(std::optional<std::string> currentSong) {
        this->currentSong = std::move(currentSong);
    }

    int getVolume() const {
        return volume;
    }
};

}  // namespace org::example