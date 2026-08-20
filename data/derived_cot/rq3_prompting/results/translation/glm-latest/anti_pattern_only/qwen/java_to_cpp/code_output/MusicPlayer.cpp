// C++17 translation of org.example.MusicPlayer.
// Java's nullable String is modeled with std::optional<std::string>
// (std::nullopt plays the role of Java null).

#include <algorithm>
#include <cstddef>
#include <iterator>
#include <optional>
#include <random>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

class MusicPlayer {
private:
    std::vector<std::string> playlist;
    std::optional<std::string> currentSong;   // std::nullopt == Java null
    int volume = 50;

    // Equivalent of java.util.List#indexOf: -1 when not present.
    std::ptrdiff_t indexOf(const std::string& song) const {
        auto it = std::find(playlist.begin(), playlist.end(), song);
        return it == playlist.end() ? static_cast<std::ptrdiff_t>(-1)
                                    : std::distance(playlist.begin(), it);
    }

public:
    MusicPlayer() = default;

    void addSong(const std::string& song) {
        playlist.push_back(song);
    }

    void removeSong(const std::string& song) {
        auto it = std::find(playlist.begin(), playlist.end(), song);
        if (it != playlist.end()) {
            playlist.erase(it);   // removes first occurrence, like List.remove(Object)
            if (currentSong.has_value() && *currentSong == song) {
                stop();
            }
        }
    }

    std::optional<std::string> play() const {
        if (playlist.empty()) {
            return std::nullopt;
        }
        if (currentSong.has_value() && indexOf(*currentSong) != -1) {
            return currentSong;
        }
        return playlist[0];
    }

    bool stop() {
        if (currentSong.has_value()) {
            currentSong.reset();
            return true;
        } else {
            return false;
        }
    }

    bool switchSong() {
        if (!currentSong.has_value()) {
            return false;
        }
        std::ptrdiff_t currentIndex = indexOf(*currentSong);
        if (currentIndex < static_cast<std::ptrdiff_t>(playlist.size()) - 1) {
            currentSong = playlist[static_cast<std::size_t>(currentIndex + 1)];
            return true;
        } else {
            return false;
        }
    }

    bool previousSong() {
        if (!currentSong.has_value()) {
            return false;
        }
        std::ptrdiff_t currentIndex = indexOf(*currentSong);
        if (currentIndex > 0) {
            currentSong = playlist[static_cast<std::size_t>(currentIndex - 1)];
            return true;
        } else {
            return false;
        }
    }

    bool setVolume(int volume) {
        if (volume >= 0 && volume <= 100) {
            this->volume = volume;
            return true;
        } else {
            return false;
        }
    }

    bool shuffle() {
        if (playlist.empty()) {
            return false;
        }
        std::shuffle(playlist.begin(), playlist.end(),
                     std::mt19937(std::random_device{}()));
        return true;
    }

    // Returns a live reference to the internal list, like the Java getter.
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

    // Corresponds to setCurrentSong(null) in Java.
    void setCurrentSong(std::nullptr_t) {
        this->currentSong = std::nullopt;
    }

    int getVolume() const {
        return volume;
    }
};

} // namespace org::example