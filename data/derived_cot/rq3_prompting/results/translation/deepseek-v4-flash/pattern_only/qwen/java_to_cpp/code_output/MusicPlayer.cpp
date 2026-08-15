#include <string>
#include <vector>
#include <optional>
#include <algorithm>
#include <random>
#include <iterator>
#include <utility>

class MusicPlayer {
private:
    std::vector<std::string> playlist;
    std::optional<std::string> currentSong;
    int volume;

public:
    MusicPlayer() : playlist(), currentSong(std::nullopt), volume(50) {}

    void addSong(const std::string& song) {
        playlist.push_back(song);
    }

    void removeSong(const std::string& song) {
        auto it = std::find(playlist.begin(), playlist.end(), song);
        if (it != playlist.end()) {
            playlist.erase(it);
            if (currentSong.has_value() && *currentSong == song) {
                stop();
            }
        }
    }

    std::optional<std::string> play() const {
        if (playlist.empty()) {
            return std::nullopt;
        }
        if (currentSong.has_value()) {
            for (const auto& song : playlist) {
                if (song == *currentSong) {
                    return currentSong;
                }
            }
        }
        return playlist.front();
    }

    bool stop() {
        if (currentSong.has_value()) {
            currentSong = std::nullopt;
            return true;
        }
        return false;
    }

    bool switchSong() {
        if (!currentSong.has_value()) {
            return false;
        }
        auto it = std::find(playlist.begin(), playlist.end(), *currentSong);
        int currentIndex = (it != playlist.end()) ? static_cast<int>(std::distance(playlist.begin(), it)) : -1;
        if (currentIndex < static_cast<int>(playlist.size()) - 1) {
            currentSong = playlist[currentIndex + 1];
            return true;
        }
        return false;
    }

    bool previousSong() {
        if (!currentSong.has_value()) {
            return false;
        }
        auto it = std::find(playlist.begin(), playlist.end(), *currentSong);
        int currentIndex = (it != playlist.end()) ? static_cast<int>(std::distance(playlist.begin(), it)) : -1;
        if (currentIndex > 0) {
            currentSong = playlist[currentIndex - 1];
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
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(playlist.begin(), playlist.end(), g);
        return true;
    }

    std::vector<std::string>& getPlaylist() {
        return playlist;
    }

    void setPlaylist(std::vector<std::string> playlist) {
        this->playlist = std::move(playlist);
    }

    std::optional<std::string> getCurrentSong() const {
        return currentSong;
    }

    void setCurrentSong(std::optional<std::string> currentSong) {
        this->currentSong = std::move(currentSong);
    }

    int getVolume() const {
        return volume;
    }
};