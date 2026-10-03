#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include <optional>

class MusicPlayer {
private:
    std::vector<std::string> playlist_;
    std::optional<std::string> currentSong_;
    int volume_;

public:
    MusicPlayer()
        : playlist_()
        , currentSong_(std::nullopt)
        , volume_(50)
    {}

    void addSong(const std::string& song) {
        playlist_.push_back(song);
    }

    void removeSong(const std::string& song) {
        auto it = std::find(playlist_.begin(), playlist_.end(), song);
        if (it != playlist_.end()) {
            playlist_.erase(it);
            if (currentSong_.has_value() && currentSong_.value() == song) {
                stop();
            }
        }
    }

    std::optional<std::string> play() {
        if (playlist_.empty()) {
            return std::nullopt;
        }
        if (currentSong_.has_value()) {
            const std::string& cur = currentSong_.value();
            if (std::find(playlist_.begin(), playlist_.end(), cur) != playlist_.end()) {
                return cur;
            }
        }
        return playlist_.front();
    }

    bool stop() {
        if (currentSong_.has_value()) {
            currentSong_.reset();
            return true;
        }
        return false;
    }

    bool switchSong() {
        if (!currentSong_.has_value()) {
            return false;
        }
        const std::string& cur = currentSong_.value();
        auto it = std::find(playlist_.begin(), playlist_.end(), cur);
        if (it == playlist_.end()) {
            return false;   // shouldn't happen, but safe guard
        }
        auto nextIt = it + 1;
        if (nextIt != playlist_.end()) {
            currentSong_ = *nextIt;
            return true;
        }
        return false;
    }

    bool previousSong() {
        if (!currentSong_.has_value()) {
            return false;
        }
        const std::string& cur = currentSong_.value();
        auto it = std::find(playlist_.begin(), playlist_.end(), cur);
        if (it == playlist_.begin() || it == playlist_.end()) {
            return false;
        }
        currentSong_ = *(it - 1);
        return true;
    }

    bool setVolume(int volume) {
        if (volume >= 0 && volume <= 100) {
            volume_ = volume;
            return true;
        }
        return false;
    }

    bool shuffle() {
        if (playlist_.empty()) {
            return false;
        }
        static std::random_device rd;
        static std::mt19937 g(rd());
        std::shuffle(playlist_.begin(), playlist_.end(), g);
        return true;
    }

    // Getters and setters – replicate Java reference semantics as closely as possible.
    // getPlaylist returns a non-const reference so that modifications through it affect the internal list.
    std::vector<std::string>& getPlaylist() {
        return playlist_;
    }

    const std::vector<std::string>& getPlaylist() const {
        return playlist_;
    }

    void setPlaylist(const std::vector<std::string>& playlist) {
        playlist_ = playlist;
    }

    std::optional<std::string> getCurrentSong() const {
        return currentSong_;
    }

    void setCurrentSong(const std::string& currentSong) {
        currentSong_ = currentSong;
    }

    int getVolume() const {
        return volume_;
    }
};